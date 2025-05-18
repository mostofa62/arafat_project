from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User, db, Course,Category
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in
import os
from flask_mail import Message
from app import mail

from flask import Blueprint, render_template
from app.middleware import redirect_if_logged_in

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
#@redirect_if_logged_in
def home():
    categories = Category.query.limit(20).all()
    app_name = os.getenv("APP_NAME", "App For All")
    return render_template('home.html', categories=categories,app_name=app_name)



@home_bp.route('/category-course/<int:category_id>')
#@redirect_if_logged_in
def category_course(category_id):
    category = Category.query.get_or_404(category_id)
    courses = Course.query.filter_by(category_id=category.id).limit(20).all()
    return render_template('category-course.html', category=category, courses=courses)

@home_bp.route('/login-all')
@redirect_if_logged_in
def login():
    return render_template('login-all.html')


@home_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('home_bp.contact'))

        msg = Message(
            subject=f"[Contact Form] {subject}",
            sender=email,
            recipients=["admin@example.com"],  # Replace with admin's email
            body=f"From: {name} <{email}>\n\n{message}"
        )
        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash("An error occurred while sending the email.", "error")
        return redirect(url_for('home_bp.contact'))

    return render_template('contact.html')


@home_bp.route('/all-courses')
def all_courses():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    courses = Course.query.order_by(Course.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('all-courses.html', courses=courses)
