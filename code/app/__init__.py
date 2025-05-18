from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from app.middleware import no_cache_middleware, CustomLoginManager, redirect_if_logged_in
from werkzeug.exceptions import RequestEntityTooLarge
from flask_babel import Babel, format_number

from flask_mail import Mail

db = SQLAlchemy()
#login_manager = LoginManager()
login_manager = CustomLoginManager()

mail = Mail()

def create_app():
    app = Flask(__name__)

    babel = Babel(app)
    app.jinja_env.filters['format_number'] = format_number

    # Apply middleware
    app = no_cache_middleware(app)
    
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    mail.init_app(app)

    # Import models after initializing extensions
    with app.app_context():
        from app.models import User
        db.create_all()  # Create database tables if they don't exist

    # Register Blueprints
    from app.views.home import home_bp
    from app.views.admin import admin_bp
    from app.views.teacher import teacher_bp
    from app.views.student import student_bp
    from app.views.admin_categories import admin_categories_bp
    from app.views.teacher_courses import teacher_courses
    from app.views.student_courses import student_courses
    from app.views.course_lesson import course_lesson
    from app.views.enrolled_lesson import enrolled_lesson
    from app.views.course_quiz import course_quiz
    from app.views.quiz_question import quiz_question

    from app.views.enrolled_quiz import enrolled_quiz
    from app.views.course_student import course_students

    from app.views.checkout import checkout_bp
    from app.views.admin_courses import admin_courses_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_categories_bp)
    app.register_blueprint(teacher_courses)
    app.register_blueprint(student_courses)
    app.register_blueprint(course_lesson)
    app.register_blueprint(enrolled_lesson)
    app.register_blueprint(course_quiz)
    app.register_blueprint(quiz_question)
    app.register_blueprint(enrolled_quiz)
    app.register_blueprint(course_students)
    app.register_blueprint(admin_courses_bp)

    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    


    # Handle file size limit exceeded
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return jsonify({"error": "File is too large. Maximum allowed size is 2 MB."}), 413

    return app

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))  # SQLAlchemy 2.x syntax for fetching by primary key
