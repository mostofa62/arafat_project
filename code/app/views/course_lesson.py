import os
import uuid
from flask import Blueprint, current_app, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.models import Course, Lesson, User, CourseProgress
from app.forms import LessonForm
from datetime import timedelta

def parse_duration(duration_str: str):
    """
    Converts a duration string in HH:mm:ss format to a timedelta object.
    Returns None if the string is empty or invalid.
    """
    if duration_str:
        try:
            h, m, s = map(int, duration_str.strip().split(":"))
            return timedelta(hours=h, minutes=m, seconds=s)
        except ValueError:
            # Invalid format, optionally raise or return None
            return None
    return None

course_lesson = Blueprint('course_lesson', __name__, template_folder='templates')

# List Lessons for a Course
@course_lesson.route('/courses/<int:course_id>/lessons', methods=['GET'])
@login_required
def list_lessons(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('teacher_courses.index'))
    
    return render_template('teacher/lessons/index.html', course=course, title=f'Lessons for {course.title}')

# API for fetching lessons data
@course_lesson.route('/courses/<int:course_id>/lessons/data', methods=['GET'])
@login_required
def lessons_data(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()

    data = []
    for lesson in lessons:
        # Check if this lesson has any progress entries
        has_progress = CourseProgress.query.filter_by(lesson_id=lesson.id).first() is not None

        actions_html = f"""
            <a href="{url_for('course_lesson.edit', course_id=course_id, lesson_id=lesson.id)}" 
               class="bg-yellow-400 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-yellow-500 text-sm">
                Edit
            </a>
        """
        if not has_progress:
            # Only show Delete if no progress exists for the lesson
            actions_html += f"""
                <button data-url="{url_for('course_lesson.delete', course_id=course_id, lesson_id=lesson.id)}" 
                        class="delete-lesson bg-red-500 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-red-600 text-sm">
                    Delete
                </button>
            """

        data.append({
            'id': lesson.id,
            'title': lesson.title,
            'content_type': lesson.content_type,
            'order': lesson.order,
            'actions': actions_html
        })

    return jsonify({"data": data})


# Create Lesson
@course_lesson.route('/courses/<int:course_id>/lessons/create', methods=['GET', 'POST'])
@login_required
def create(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('course_lesson.list_lessons', course_id=course_id))

    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            course_id=course_id,
            title=form.title.data,
            content_type=form.content_type.data,
            content_url=form.content_url.data,
            text_content=form.text_content.data,
            duration=parse_duration(form.duration.data),
            order=form.order.data,
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Lesson created successfully!', 'success')
        return redirect(url_for('course_lesson.list_lessons', course_id=course_id))

    return render_template('teacher/lessons/form.html', form=form, course=course, title=f'Create Lesson for {course.title}')

# Edit Lesson
@course_lesson.route('/courses/<int:course_id>/lessons/edit/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def edit(course_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('course_lesson.list_lessons', course_id=course_id))

    form = LessonForm(obj=lesson)
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.content_type = form.content_type.data
        lesson.content_url = form.content_url.data
        lesson.text_content = form.text_content.data
        lesson.duration =  parse_duration(form.duration.data)
        lesson.order = form.order.data
        db.session.commit()
        flash('Lesson updated successfully!', 'success')
        return redirect(url_for('course_lesson.list_lessons', course_id=course_id))

    return render_template('teacher/lessons/form.html', form=form, course=course, lesson=lesson, title='Edit Lesson')

# Delete Lesson
@course_lesson.route('/courses/<int:course_id>/lessons/delete/<int:lesson_id>', methods=['POST'])
@login_required
def delete(course_id, lesson_id):    
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    if course.teacher_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    
    # Save content_url before deleting lesson
    content_url = lesson.content_url

    db.session.delete(lesson)
    db.session.commit()

    if content_url:
        final_filepath = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'coureselesson',  # Note: is 'coureselesson' intentional or should it be 'courselesson'?
            str(course_id),
            content_url
        )
        if os.path.exists(final_filepath):
            os.remove(final_filepath)
    return jsonify({"success": True})



from app.utils import allowed_file_lessson
from werkzeug.utils import secure_filename
@course_lesson.route('/courses/<int:course_id>/upload-lesson-content', methods=['POST'])
@login_required
def upload_lesson_content(course_id):
    try:
        # Validate the required fields
        chunk = request.files.get('file')
        total_chunks = request.form.get('total_chunks', type=int)
        chunk_index = request.form.get('chunk_index', type=int)
        file_id = request.form.get('file_id') or uuid.uuid4().hex
        filename = request.form.get('filename')

        if not chunk or not filename or total_chunks is None or chunk_index is None:
            return jsonify({"error": "Invalid request parameters"}), 400

        # Validate the file type
        if not allowed_file_lessson(filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Validate the chunk size
        max_chunk_size = current_app.config['MAX_CONTENT_LENGTH']  # 2 MB
        if chunk.content_length > max_chunk_size:
            return jsonify({"error": "Chunk size exceeds 2 MB"}), 413

        # Temporary storage path
        temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', file_id)
        os.makedirs(temp_dir, exist_ok=True)

        # Save the chunk
        chunk_path = os.path.join(temp_dir, f"chunk_{chunk_index}")
        chunk.save(chunk_path)

        # If all chunks are received, assemble the file
        if chunk_index + 1 == total_chunks:
            final_filename = f"{uuid.uuid4().hex}_{secure_filename(filename)}"

            final_filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                'coureselesson',
                str(course_id)
            )

            # Create the directory if it doesn't exist
            os.makedirs(final_filepath, exist_ok=True)

            # Add the filename to the path
            final_filepath = os.path.join(final_filepath, final_filename)


            with open(final_filepath, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(temp_dir, f"chunk_{i}")
                    with open(chunk_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

            # Clean up temporary chunks
            for i in range(total_chunks):
                os.remove(os.path.join(temp_dir, f"chunk_{i}"))
            os.rmdir(temp_dir)           

            #return jsonify({"filepath": f"static/uploads/{final_filename}"}), 200
            return jsonify({
                "filepath": f"static/uploads/{final_filename}", 
                "filename": final_filename,
                "content_url": url_for('static', filename=f'uploads/coureselesson/{course_id}/{final_filename}')
                }), 200

        return jsonify({"message": "Chunk uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
