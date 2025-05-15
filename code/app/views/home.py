from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User, db, Course,Category
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in
import os


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


@home_bp.route('/contact')
def contact():
    return ""