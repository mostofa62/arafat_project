from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required
from app import db
from app.models import Course, Enrollment
import os
from  datetime import datetime
from sqlalchemy import func
admin_courses_bp = Blueprint('admin_courses', __name__, url_prefix='/admin/courses')



@admin_courses_bp.route('/data', methods=['GET'])
@login_required
def admin_courses_data():
    # Subquery for enrollment counts
    enrollment_counts_subq = (
        db.session.query(
            Enrollment.course_id,
            func.count(Enrollment.id).label('enrollment_count')
        )
        .group_by(Enrollment.course_id)
        .subquery()
    )

    query = (
        db.session.query(
            Course,
            func.coalesce(enrollment_counts_subq.c.enrollment_count, 0).label('enrollment_count')
        )
        .outerjoin(enrollment_counts_subq, Course.id == enrollment_counts_subq.c.course_id)
    )

    # Optional search
    search_value = request.args.get('search[value]')
    if search_value:
        query = query.filter(Course.title.ilike(f'%{search_value}%'))

    # Sorting
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

    # Format response
    data = []
    for course, enrollment_count in courses:
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
            "price": f"${course.price:.2f}",
            "created_at": course.created_at.strftime('%b %d, %Y'),
            "enrollment_count": enrollment_count           
        })

    return jsonify({
        "draw": request.args.get('draw', 1),
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })


@admin_courses_bp.route('/')
@login_required
def index():
    return render_template('admin/courses/index.html', title='All Courses')