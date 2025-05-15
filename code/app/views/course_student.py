import os
import uuid
from flask import Blueprint, current_app, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.models import Course, Lesson, User, CourseProgress, Enrollment
from datetime import timedelta
from sqlalchemy import or_, asc, desc, func
from sqlalchemy.orm import aliased
course_students = Blueprint('course_students', __name__, template_folder='templates')

@course_students.route('/courses/students/data', methods=['GET'])
@login_required
def course_students_data():
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str, default='').strip()

    order_column_index = request.args.get('order[0][column]', type=int)
    order_direction = request.args.get('order[0][dir]', type=str, default='asc')

    # Subquery for courses taught by the current teacher
    teacher_courses_subq = (
        db.session.query(Course.id)
        .filter(Course.teacher_id == current_user.id)
        .subquery()
    )

    # Subquery for lesson counts per course
    lesson_counts_subq = (
        db.session.query(
            Lesson.course_id.label('course_id'),
            func.count(Lesson.id).label('total_lessons')
        )
        .filter(Lesson.course_id.in_(teacher_courses_subq.select()))
        .group_by(Lesson.course_id)
        .subquery()
    )

    # Main query
    base_query = (
        db.session.query()
        .with_entities(
            Enrollment.id.label('enrollment_id'),
            User.name.label('student_name'),
            Course.title.label('course_title'),
            Course.id.label('course_id'),
            func.count(CourseProgress.id).label('completed_lessons'),
            lesson_counts_subq.c.total_lessons
        )
        .join(User, User.id == Enrollment.student_id)
        .join(Course, Course.id == Enrollment.course_id)
        .outerjoin(CourseProgress, 
            (CourseProgress.student_id == Enrollment.student_id) &
            (CourseProgress.course_id == Enrollment.course_id)
        )
        .outerjoin(lesson_counts_subq, lesson_counts_subq.c.course_id == Course.id)
        .filter(Course.teacher_id == current_user.id)
        .group_by(Enrollment.id, User.name, Course.title, Course.id, lesson_counts_subq.c.total_lessons)
    )

    # Total records before filtering
    total_records = base_query.count()

    # Global search filter
    if search_value:
        base_query = base_query.filter(or_(
            User.name.ilike(f"%{search_value}%"),
            Course.title.ilike(f"%{search_value}%")
        ))

    # Filtered record count
    records_filtered = base_query.count()

    # Column ordering mapping to SQLAlchemy expressions
    column_map = {
        0: User.name,
        1: Course.title,
        2: func.count(CourseProgress.id),
        3: lesson_counts_subq.c.total_lessons,
    }

    # Apply ordering
    col = column_map.get(order_column_index)
    if col is not None:
        direction_func = asc if order_direction == 'asc' else desc
        base_query = base_query.order_by(direction_func(col))

    # Pagination
    results = base_query.offset(start).limit(length).all()

    # Response data formatting
    data = []
    for row in results:
        total_lessons = row.total_lessons or 0
        completed = int(row.completed_lessons)
        progress_percent = round((completed / total_lessons) * 100, 2) if total_lessons else 0

        data.append({
            "student_name": row.student_name,
            "course_title": row.course_title,
            "completed_lessons": completed,
            "total_lessons": total_lessons,
            "progress_percent": f"{progress_percent:.2f}%"
        })

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": records_filtered,
        "data": data
    })

@course_students.route('/courses/students', methods=['GET'])
@login_required
def index():        
    return render_template('teacher/students/index.html', title=f'Course Enrollments')