from flask import Blueprint, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.models import Course, Lesson
from app.forms import LessonForm

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
    data = [
        {
            'id': lesson.id,
            'title': lesson.title,
            'content_type': lesson.content_type,
            'order': lesson.order,
            'actions': f"""
                <a href="{url_for('course_lesson.edit', course_id=course_id, lesson_id=lesson.id)}" 
                   class="bg-yellow-400 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-yellow-500 text-sm">
                    Edit
                </a>
                <button data-url="{url_for('course_lesson.delete', course_id=course_id, lesson_id=lesson.id)}" 
                        class="delete-lesson bg-red-500 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-red-600 text-sm">
                    Delete
                </button>
            """
        }
        for lesson in lessons
    ]
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
            video_url=form.video_url.data,
            duration=form.duration.data,
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
        lesson.video_url = form.video_url.data
        lesson.duration = form.duration.data
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

    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"success": True})
