from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Course, Enrollment, Quiz, QuizAttempt
from app.forms import QuizForm  # You'll need to create this form
from datetime import datetime

enrolled_quiz = Blueprint('enrolled_quiz', __name__, template_folder='templates')


@enrolled_quiz.route('/enrollments/<int:course_id>/quizzes', methods=['GET'])
@login_required
def list_quizzes(course_id):
    enrollment = Enrollment.query.filter_by(course_id=course_id, student_id=current_user.id).first()
    
    if not enrollment:
        #flash('You are not enrolled in this course.', 'danger')
        return redirect(url_for('student_courses.index'))
    course = enrollment.course
    return render_template('student/quizzes/index.html', course=course, title=f'Quizzes for {course.title}')



@enrolled_quiz.route('/enrollments/<int:course_id>/quizzes/data', methods=['GET'])
@login_required
def quizzes_data(course_id):
    enrollment = Enrollment.query.filter_by(course_id=course_id, student_id=current_user.id).first()
    if not enrollment or enrollment.student_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    quizzes = Quiz.query.filter_by(course_id=enrollment.course_id).order_by(Quiz.created_at.desc()).all()

    data = []
    for quiz in quizzes:
        attempt = QuizAttempt.query.filter_by(
            quiz_id=quiz.id,
            student_id=current_user.id
        ).first()

        data.append({
            'id': quiz.id,
            'title': quiz.title,
            'score': f"{attempt.score}%" if attempt and attempt.score is not None else None
        })

    return jsonify({"data": data})




