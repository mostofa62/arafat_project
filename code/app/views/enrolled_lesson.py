import os
import uuid
from flask import Blueprint, abort, current_app, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import asc
from app import db
from app.models import Course, Enrollment, Lesson, User,CourseProgress
from app.forms import LessonForm
from datetime import timedelta
from sqlalchemy.orm import joinedload

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

enrolled_lesson = Blueprint('enrolled_lesson', __name__, template_folder='templates')

# List Lessons for a Course
@enrolled_lesson.route('/enrollments/<int:course_id>/lessons', methods=['GET'])
@login_required
def list_lessons(course_id):
    # Check if the current user is enrolled in the course
    enrollment = Enrollment.query.filter_by(course_id=course_id, student_id=current_user.id).first()
    
    if not enrollment:
        #flash('You are not enrolled in this course.', 'danger')
        return redirect(url_for('student_courses.index'))

    course = enrollment.course  # You can access the course from the relationship
    return render_template('student/lessons/index.html', course=course, title=f'Lessons for {course.title}')

@enrolled_lesson.route('/enrollments/<int:course_id>/lessons/data', methods=['GET'])
@login_required
def lessons_data(course_id):
    enrollment = Enrollment.query.filter_by(course_id=course_id, student_id=current_user.id).first()
    if not enrollment:
        return jsonify({"error": "No Enrollments lessons"}), 403

    # Query lessons and progress in one go
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(asc(Lesson.order)).all()
    completed_lesson_ids = {
        cp.lesson_id for cp in CourseProgress.query.filter_by(course_id=course_id, student_id=current_user.id).all()
    }

    data = [
        {
            'id': lesson.id,
            'title': lesson.title,
            'content_type': lesson.content_type,
            'order': lesson.order,
            'completed': lesson.id in completed_lesson_ids,
            'actions': f"""
                <a href="{url_for('enrolled_lesson.show', course_id=course_id, lesson_id=lesson.id)}" 
                   class="bg-yellow-400 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-yellow-500 text-sm">
                  Show  
                </a>
            """
        }
        for lesson in lessons
    ]
    return jsonify({"data": data})

@enrolled_lesson.route('/enrollments/<int:course_id>/lessons/<int:lesson_id>', methods=['GET'])
@login_required
def show(course_id, lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id, course_id=course_id).first()
    if not lesson:
        abort(404)

    completed = CourseProgress.query.filter_by(
        student_id=current_user.id,
        course_id=course_id,
        lesson_id=lesson_id
    ).first()


    return render_template("student/lessons/show.html", lesson=lesson, completed=completed)


@enrolled_lesson.route('/enrollments/<int:course_id>/lessons/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(course_id, lesson_id):
    

    # Avoid duplicate entries
    existing = CourseProgress.query.filter_by(
        student_id=current_user.id,
        course_id=course_id,
        lesson_id=lesson_id
    ).first()

    if not existing:
        progress = CourseProgress(
            student_id=current_user.id,
            course_id=course_id,
            lesson_id=lesson_id
        )
        db.session.add(progress)
        db.session.commit()

    return redirect(url_for('enrolled_lesson.show', course_id=course_id, lesson_id=lesson_id))