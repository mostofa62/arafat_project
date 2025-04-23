from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Course, Category, Enrollment
from app.forms import CourseForm
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os

teacher_courses = Blueprint('teacher_courses', __name__)


@teacher_courses.route('/courses/data', methods=['GET'])
@login_required
def courses_data():

    # Subquery to get enrollment counts
    enrollment_counts_subq = (
        db.session.query(
            Enrollment.course_id,
            func.count(Enrollment.id).label('enrollment_count')
        )
        .group_by(Enrollment.course_id)
        .subquery()
    )
   # Join Course with the subquery for counts
    query = (
        db.session.query(
            Course,
            func.coalesce(enrollment_counts_subq.c.enrollment_count, 0).label('enrollment_count')
        )
        .outerjoin(enrollment_counts_subq, Course.id == enrollment_counts_subq.c.course_id)
        .filter(Course.teacher_id == current_user.id)
    )    
    # Handle search, ordering, and pagination (from DataTables parameters)
    search_value = request.args.get('search[value]')
    if search_value:
        query = query.filter(Course.title.ilike(f'%{search_value}%'))

    order_column = request.args.get('order[0][column]')
    order_dir = request.args.get('order[0][dir]')
    column_map = {
        '0': Course.id,
        '1': Course.title,
        '2': func.coalesce(Course.category_id, 'Uncategorized'),
        '3': Course.price,
        '4': Course.created_at,
        '5': 'enrollment_count'
    }
    if order_column and order_dir:
        order_by = column_map.get(order_column, Course.id)
        if order_by == 'enrollment_count':
            query = query.order_by(db.desc('enrollment_count') if order_dir == 'desc' else db.asc('enrollment_count'))
        else:
            query = query.order_by(order_by.desc() if order_dir == 'desc' else order_by)

    # Pagination
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    total_records = query.count()
    courses = query.offset(start).limit(length).all()

    # Prepare response
    data = []
    for course, enrollment_count  in courses:
        thumbnail_url = url_for('static', filename='images/default_thumb.png')
        if course.thumbnail:  # Check if the course has a thumbnail set
            thumbnail_path = os.path.join(current_app.static_folder, f'uploads/course_thumb/{course.thumbnail}')
            if os.path.exists(thumbnail_path):  # Check if the file exists
                thumbnail_url = url_for('static', filename=f'uploads/course_thumb/{course.thumbnail}')            
        

        data.append({
            "thumbnail": thumbnail_url,
            "id": course.id,
            "title": course.title,
            "category": course.category.name if course.category else "Uncategorized",
            "price": f"${course.price:.2f}",
            "created_at": course.created_at.strftime('%b %d, %Y'),            
            "enrollment_count": enrollment_count,
            "actions": f"""
                <a href="{url_for('teacher_courses.edit', id=course.id)}" class="bg-yellow-500 text-white px-2 py-1 rounded-md">Edit</a>
                <form action="{url_for('teacher_courses.delete', id=course.id)}" method="POST" style="display: inline;">
                    <button type="submit" class="bg-red-500 text-white px-2 py-1 rounded-md" onclick="return confirm('Are you sure?')">Delete</button>
                </form>
            """
        })

    return jsonify({
        "draw": request.args.get('draw', 1),
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })

# List courses (DataTable view)
@teacher_courses.route('/courses')
@login_required
def index():    
    return render_template('teacher/courses/index.html', title='My Courses')

# Helper function to save thumbnail with validation
def save_thumbnail(course_id, file):
    if file:
        # Allowed extensions
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        max_file_size = current_app.config['THUMB_CONTENT_LENGTH']

        ALLOWED_EXTENSIONS_STR = ', '.join(allowed_extensions)

        # Check file extension
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_extension not in allowed_extensions:
            raise ValueError(f'Invalid file extension. Allowed extensions are: {ALLOWED_EXTENSIONS_STR}')

        # Check file size
        file.seek(0, os.SEEK_END)  # Move to the end of the file to get its size
        file_size = file.tell()  # Get the current position (file size in bytes)
        file.seek(0)  # Reset file pointer to the beginning
        if file_size > max_file_size:
            raise ValueError('File size exceeds the 1MB limit')

        # Generate the filename using the course ID and original file name
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{course_id}_{filename}"

        # Save the file
        course_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'course_thumb')
        filepath = os.path.join(course_dir, new_filename)
        os.makedirs(course_dir, exist_ok=True)
        file.save(filepath)
        return new_filename

    return None


# Create course
@teacher_courses.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CourseForm()
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        try:
            # Save course first (without the thumbnail)
            course = Course(
                title=form.title.data,
                description=form.description.data,
                teacher_id=current_user.id,
                price=form.price.data,
                language=form.language.data,
                level=form.level.data,
                category_id=form.category_id.data,
            )
            db.session.add(course)
            db.session.commit()  # Commit to get the course.id

            # Now save the thumbnail with the course ID
            if form.thumbnail.data:
                thumbnail_filename = save_thumbnail(course.id, form.thumbnail.data)
                course.thumbnail = thumbnail_filename
                db.session.commit()  # Update the course with the thumbnail filename

            flash('Course created successfully!', 'success')
            return redirect(url_for('teacher_courses.index'))
        except ValueError as e:
            flash(str(e), 'error')

    return render_template('teacher/courses/form.html', form=form, title='Create Course')

# Edit course
@teacher_courses.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    course = Course.query.get_or_404(id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('teacher_courses.index'))
    
    form = CourseForm(obj=course)
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        try:
            # Check if a new thumbnail is uploaded and delete the old one if exists
            if form.thumbnail.data:
                # If the course already has a thumbnail, delete the old one
                if course.thumbnail:
                    old_thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'course_thumb', course.thumbnail)
                    if os.path.exists(old_thumbnail_path):
                        os.remove(old_thumbnail_path)

                # Save the new thumbnail and update the course record
                thumbnail_filename = save_thumbnail(course.id, form.thumbnail.data)
                course.thumbnail = thumbnail_filename

            # Update other course fields
            course.title = form.title.data
            course.description = form.description.data
            course.price = form.price.data
            course.language = form.language.data
            course.level = form.level.data
            course.category_id = form.category_id.data

            # Commit the changes
            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('teacher_courses.index'))
        except ValueError as e:
            flash(str(e), 'error')

    return render_template('teacher/courses/form.html', form=form, course=course, title='Edit Course')


# Delete course
@teacher_courses.route('/courses/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    course = Course.query.get_or_404(id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('teacher_courses.index'))
    
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('teacher_courses.index'))
