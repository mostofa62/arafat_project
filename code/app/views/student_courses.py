from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app , send_file
from flask_login import current_user, login_required
from app import db
from app.models import Course, Category, CourseProgress, Enrollment, Lesson, Quiz, QuizAttempt
from app.forms import CourseForm
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

from io import BytesIO
from datetime import datetime
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

        # Total quizzes in the course
        total_quizzes = Quiz.query.filter_by(course_id=course.id).count()

        # Quizzes attempted by the student in this course
        attempted_quiz_ids = db.session.query(QuizAttempt.quiz_id).join(Quiz).filter(
            Quiz.course_id == course.id,
            QuizAttempt.student_id == current_user.id
        ).distinct().count()
        
        data.append({
            "thumbnail": thumbnail_url,
            "id": course.id,
            "title": course.title,
            "category": course.category.name if course.category else "Uncategorized",
            #"price": f"${course.price:.2f}",
            "enrolled_at": enrollment.enrolled_at.strftime('%b %d, %Y'),
            "progress": f"{progress_percent}%",
            "quizzes_total": total_quizzes,
            "quizzes_attempted": attempted_quiz_ids,
            "quizzes_completed_percent": f"{round((attempted_quiz_ids / total_quizzes) * 100) if total_quizzes else 0}%",            
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



@student_courses.route('/enrollments/<int:course_id>/certificate')
@login_required
def download_certificate(course_id):
    course = Course.query.get_or_404(course_id)

    # Validate enrollment and course completion
    enrollment = Enrollment.query.filter_by(course_id=course.id, student_id=current_user.id).first()
    total_lessons = Lesson.query.filter_by(course_id=course.id).count()
    completed_lessons = CourseProgress.query.filter_by(course_id=course.id, student_id=current_user.id).count()

    if not enrollment or total_lessons == 0 or completed_lessons < total_lessons:
        flash("You must complete the course to download the certificate.", "warning")
        return redirect(url_for('student_courses.index'))

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"{course.title} - Certificate of Completion")
    width, height = letter

    # === Background Image ===
    bg_path = os.path.join(current_app.static_folder, 'images/certificate_bg.jpg')
    if os.path.exists(bg_path):
        bg = ImageReader(bg_path)
        pdf.drawImage(bg, 0, 0, width=width, height=height)
    
    
    # === Logo ===
    logo_path = os.path.join(current_app.static_folder, 'images/logo.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_x = width / 2 - 90
        logo_y = height - 360  # adjusted Y position
        logo_width = 40
        pdf.drawImage(logo, logo_x, logo_y, width=logo_width, preserveAspectRatio=True, mask='auto')

        # === App Title beside Logo ===
        app_name = os.getenv('app_name', 'Default App Name')  # Replace with your app name
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.HexColor("#333333"))  # Optional: set a custom color
        text_x = logo_x + logo_width + 10
        text_y = height - 110  # align vertically with the logo
        pdf.drawString(text_x, text_y, app_name)

    # === Certificate Content ===
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(width / 2, height - 220, "Certificate of Completion")

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 260, "This certifies that")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 315, current_user.name)

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 350, "has successfully completed the course")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 415, course.title)

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, height - 460, f"Date: {datetime.now().strftime('%B %d, %Y')}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        #as_attachment=True,
        as_attachment=False,
        download_name=f"certificate_{course.title.replace(' ', '_')}.pdf",
        mimetype='application/pdf'
    )