from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Course, Quiz, QuizAttempt
from app.forms import QuizForm  # You'll need to create this form
from datetime import datetime

course_quiz = Blueprint('course_quiz', __name__, template_folder='templates')


@course_quiz.route('/courses/<int:course_id>/quizzes', methods=['GET'])
@login_required
def list_quizzes(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('teacher_courses.index'))

    return render_template('teacher/quizzes/index.html', course=course, title=f'Quizzes for {course.title}')



@course_quiz.route('/courses/<int:course_id>/quizzes/data', methods=['GET'])
@login_required
def quizzes_data(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    quizzes = Quiz.query.filter_by(course_id=course_id).order_by(Quiz.created_at.desc()).all()

    data = []
    for quiz in quizzes:
        # Check if quiz has any attempts
        has_attempts = QuizAttempt.query.filter_by(quiz_id=quiz.id).first() is not None

        actions_html = f"""
            <a href="/quiz/{quiz.id}/questions" 
               class="inline-block bg-green-500 text-white px-3 py-1 rounded-md shadow-sm hover:bg-blue-600">
                Manage Questions
            </a>

            <a href="/quiz/{quiz.id}/attempts" 
               class="inline-block bg-blue-500 text-white px-3 py-1 rounded-md shadow-sm hover:bg-blue-600">
                Manage Submission
            </a>

            <a href="{url_for('course_quiz.edit_quiz', course_id=course_id, quiz_id=quiz.id)}" 
               class="bg-yellow-400 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-yellow-500 text-sm">
                Edit
            </a>
        """

        if not has_attempts:
            # Only show delete button if no attempts exist
            actions_html += f"""
                <button data-url="{url_for('course_quiz.delete_quiz', course_id=course_id, quiz_id=quiz.id)}" 
                        class="delete-quiz bg-red-500 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-red-600 text-sm">
                    Delete
                </button>
            """

        data.append({
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description or '',
            'created_at': quiz.created_at.strftime('%Y-%m-%d %H:%M'),
            'actions': actions_html
        })

    return jsonify({"data": data})



@course_quiz.route('/courses/<int:course_id>/quizzes/create', methods=['GET', 'POST'])
@login_required
def create_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))

    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(
            course_id=course_id,
            title=form.title.data,
            description=form.description.data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))

    return render_template('teacher/quizzes/form.html', form=form, course=course, title=f'Create Quiz for {course.title}')



@course_quiz.route('/courses/<int:course_id>/quizzes/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quiz(course_id, quiz_id):
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)

    if course.teacher_id != current_user.id or quiz.course_id != course_id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))

    form = QuizForm(obj=quiz)
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.updated_at = datetime.now()
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))

    return render_template('teacher/quizzes/form.html', form=form, course=course, quiz=quiz, title=f'Edit Quiz: {quiz.title}')



@course_quiz.route('/courses/<int:course_id>/quizzes/<int:quiz_id>/delete', methods=['POST'])
@login_required
def delete_quiz(course_id, quiz_id):
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)

    if course.teacher_id != current_user.id or quiz.course_id != course_id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))

    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('course_quiz.list_quizzes', course_id=course_id))
