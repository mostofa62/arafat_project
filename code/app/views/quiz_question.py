from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Answer, AttemptAnswer, Quiz,Question, QuizAttempt
from app.forms import QuestionForm  # You'll need to create this form
from datetime import datetime


quiz_question = Blueprint('quiz_question', __name__, template_folder='templates')

@quiz_question.route('/quiz/<int:quiz_id>/questions', methods=['GET'])
@login_required
def list_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('course_quiz.list_quizzes', course_id=quiz.course.id))

    return render_template('teacher/quizzes/questions/index.html', quiz=quiz, title=f'Questions for {quiz.title}')


@quiz_question.route('/quiz/<int:quiz_id>/questions/data', methods=['GET'])
@login_required
def questions_data(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.course.teacher_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id.desc()).all()
    data = [
        {
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type.replace('_', ' ').title(),
            'actions': f"""
                <a href="{url_for('quiz_question.edit_question', quiz_id=quiz.id, question_id=question.id)}" 
                   class="bg-yellow-400 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-yellow-500 text-sm">
                    Edit
                </a>
                <button data-url="{url_for('quiz_question.delete_question', quiz_id=quiz.id, question_id=question.id)}" 
                        class="delete-question bg-red-500 text-white px-3 py-1 rounded-sm shadow-sm hover:bg-red-600 text-sm">
                    Delete
                </button>
            """
        }
        for question in questions
    ]
    return jsonify({"data": data})


@quiz_question.route('/quiz/<int:quiz_id>/questions/create', methods=['GET', 'POST'])
@login_required
def create_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('quiz_question.list_quizzes', course_id=quiz.course.id))

    form = QuestionForm()

    if form.validate_on_submit():
        if form.question_type.data == 'single_choice':
            correct_answers = [a for a in form.answer_texts.entries if a.form.is_correct.data]
            if len(correct_answers) != 1:
                flash('Single choice question must have exactly one correct answer.', 'error')
                return render_template('teacher/quizzes/questions/form.html', form=form, quiz=quiz, title='Create Question')

        question = Question(
            quiz_id=quiz.id,
            question_text=form.question_text.data,
            question_type=form.question_type.data,
            created_at=datetime.now()
        )
        db.session.add(question)
        db.session.flush()

        for answer_form in form.answer_texts.entries:
            db.session.add(Answer(
                question_id=question.id,
                answer_text=answer_form.form.answer_text.data,
                is_correct=answer_form.form.is_correct.data
            ))

        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('quiz_question.list_questions', quiz_id=quiz.id))

    return render_template('teacher/quizzes/questions/form.html', form=form, quiz=quiz, title='Create Question')



@quiz_question.route('/quiz/<int:quiz_id>/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    if quiz.course.teacher_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('quiz_question.list_quizzes', course_id=quiz.course.id))

    form = QuestionForm(obj=question)

    if request.method == 'GET':
        while len(form.answer_texts) < len(question.answers):
            form.answer_texts.append_entry()
        for i, answer in enumerate(question.answers):
            form.answer_texts[i].form.answer_text.data = answer.answer_text
            form.answer_texts[i].form.is_correct.data = answer.is_correct

    if form.validate_on_submit():
        if form.question_type.data == 'single_choice':
            correct_answers = [a for a in form.answer_texts.entries if a.form.is_correct.data]
            if len(correct_answers) != 1:
                flash('Single choice question must have exactly one correct answer.', 'error')
                return render_template('teacher/quizzes/questions/form.html', form=form, quiz=quiz, question=question, title='Edit Question')

        question.question_text = form.question_text.data
        question.question_type = form.question_type.data
        db.session.commit()

        # Remove old answers
        Answer.query.filter_by(question_id=question.id).delete()

        # Add new answers
        for answer_form in form.answer_texts.entries:
            db.session.add(Answer(
                question_id=question.id,
                answer_text=answer_form.form.answer_text.data,
                is_correct=answer_form.form.is_correct.data
            ))

        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('quiz_question.list_questions', quiz_id=quiz_id))

    return render_template('teacher/quizzes/questions/form.html', form=form, quiz=quiz, question=question, title='Edit Question')



@quiz_question.route('/quiz/<int:quiz_id>/questions/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    if quiz.course.teacher_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    db.session.delete(question)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Question deleted successfully'})



@quiz_question.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # ✅ Check if the student already attempted this quiz
    existing_attempt = QuizAttempt.query.filter_by(
        quiz_id=quiz_id,
        student_id=current_user.id
    ).first()

    if existing_attempt:
        flash('You have already attempted this quiz.', 'warning')
        return redirect(url_for('enrolled_quiz.list_quizzes', course_id=quiz.course_id))

    if request.method == 'POST':
        # Create the quiz attempt
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            student_id=current_user.id
        )
        db.session.add(attempt)
        db.session.flush()  # So we get the attempt.id

        total_questions = 0
        correct_answers = 0

        for question in quiz.questions:
            qid = str(question.id)
            selected_ids = request.form.getlist(f'question-{qid}')

            for selected_id in selected_ids:
                selected_answer = Answer.query.get(int(selected_id))
                if selected_answer and selected_answer.question_id == question.id:
                    db.session.add(AttemptAnswer(
                        attempt_id=attempt.id,
                        question_id=question.id,
                        selected_answer_id=selected_answer.id
                    ))

                    if selected_answer.is_correct:
                        correct_answers += 1

            total_questions += 1

        # Save score
        if total_questions:
            attempt.score = round((correct_answers / total_questions) * 100, 2)
        db.session.commit()

        flash(f'Quiz submitted! Your score: {attempt.score}%', 'success')
        return redirect(url_for('enrolled_quiz.list_quizzes', course_id=quiz.course_id))

    # GET: render quiz form
    return render_template('student/quizzes/attempt.html', quiz=quiz)




@quiz_question.route('/quiz/<int:quiz_id>/result', methods=['GET'])
@login_required
def quiz_result(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Ensure the student has attempted the quiz
    attempt = QuizAttempt.query.filter_by(quiz_id=quiz_id, student_id=current_user.id).first()
    if not attempt:
        flash("You haven't attempted this quiz yet.", "warning")
        return redirect(url_for('enrolled_quiz.list_quizzes', course_id=quiz.course_id))

    result_data = []

    for question in quiz.questions:
        selected_answers = AttemptAnswer.query.filter_by(attempt_id=attempt.id, question_id=question.id).all()
        selected_ids = {sa.selected_answer_id for sa in selected_answers}

        all_answers = Answer.query.filter_by(question_id=question.id).all()
        correct_ids = {a.id for a in all_answers if a.is_correct}

        result_data.append({
            'question_text': question.question_text,
            'answers': [
                {
                    'text': a.answer_text,
                    'is_correct': a.id in correct_ids,
                    'is_selected': a.id in selected_ids
                } for a in all_answers
            ]
        })

    return render_template('student/quizzes/result.html', quiz=quiz, result_data=result_data, score=attempt.score)






@quiz_question.route('/quiz/<int:quiz_id>/attempts', methods=['GET'])
@login_required
def quiz_attempts(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Optional permission check (adjust as needed)
    if current_user.role != 'teacher':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('course_quiz.list_quizzes', course_id=quiz.course_id))

    return render_template('teacher/quizzes/attempts.html', quiz=quiz, title=f'Attempts for {quiz.title}')



@quiz_question.route('/quiz/<int:quiz_id>/attempts/data', methods=['GET'])
@login_required
def quiz_attempts_data(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if current_user.role != 'teacher':
        return jsonify({"error": "Unauthorized access"}), 403

    attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).order_by(QuizAttempt.attempted_at.desc()).all()
    data = [
        {
            #"id": attempt.id,
            "student_name": attempt.student.name,
            "score": attempt.score if attempt.score is not None else "Not graded",
            "attempted_at": attempt.attempted_at.strftime('%d %b, %Y %H:%M'),
            "student_id": attempt.student_id,
            "quiz_id":attempt.quiz_id
        }
        for attempt in attempts
    ]
    return jsonify({"data": data})



@quiz_question.route('/quiz/<int:quiz_id>/<int:student_id>/result', methods=['GET'])
@login_required
def student_quiz_result_(quiz_id, student_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    attempt = QuizAttempt.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
    if not attempt:
        flash("This student hasn't attempted the quiz yet.", "warning")
        return redirect(url_for('course_quiz.list_quizzes', course_id=quiz.course_id))

    result_data = []

    for question in quiz.questions:
        selected_answers = AttemptAnswer.query.filter_by(attempt_id=attempt.id, question_id=question.id).all()
        selected_ids = {sa.selected_answer_id for sa in selected_answers}

        all_answers = Answer.query.filter_by(question_id=question.id).all()
        correct_ids = {a.id for a in all_answers if a.is_correct}

        result_data.append({
            'question_text': question.question_text,
            'answers': [
                {
                    'text': a.answer_text,
                    'is_correct': a.id in correct_ids,
                    'is_selected': a.id in selected_ids
                } for a in all_answers
            ]
        })

    return render_template(
        'student/quizzes/result.html',
        quiz=quiz,
        result_data=result_data,
        score=attempt.score,
        student_id=student_id
    )

