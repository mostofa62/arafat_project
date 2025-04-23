from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Course, Category, CourseProgress, Enrollment, Lesson
from app.forms import CourseForm
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os

student_courses = Blueprint('student_courses', __name__)


@student_courses.route('/enrollments/data', methods=['GET'])
@login_required
def courses_data():
    # Get the enrolled courses for the current user
    query = Enrollment.query.join(Course).filter(Enrollment.student_id == current_user.id)

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
    }
    if order_column and order_dir:
        order_by = column_map.get(order_column, Course.id)
        query = query.order_by(order_by.desc() if order_dir == 'desc' else order_by)

    # Pagination
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    total_records = query.count()
    enrollments = query.offset(start).limit(length).all()

    # Prepare response
    data = []
    for enrollment in enrollments:
        course = enrollment.course

        # Course progress calculation
        total_lessons = Lesson.query.filter_by(course_id=course.id).count()
        completed_lessons = CourseProgress.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).count()

        progress_percent = 0
        if total_lessons > 0:
            progress_percent = round((completed_lessons / total_lessons) * 100)

            
        thumbnail_url = url_for('static', filename='images/default_thumb.png')
        if course.thumbnail:
            thumbnail_path = os.path.join(current_app.static_folder, f'uploads/course_thumb/{course.thumbnail}')
            if os.path.exists(thumbnail_path):
                thumbnail_url = url_for('static', filename=f'uploads/course_thumb/{course.thumbnail}')

        data.append({
            "thumbnail": thumbnail_url,
            "id": course.id,
            "title": course.title,
            "category": course.category.name if course.category else "Uncategorized",
            #"price": f"${course.price:.2f}",
            "enrolled_at": enrollment.enrolled_at.strftime('%b %d, %Y'),
            "progress": f"{progress_percent}%"            
        })

    return jsonify({
        "draw": request.args.get('draw', 1),
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })

# List courses (DataTable view)
@student_courses.route('/enrollments')
@login_required
def index():    
    return render_template('student/enrollments/index.html', title='My Enrollments')



