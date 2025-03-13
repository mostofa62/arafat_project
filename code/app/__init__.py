from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.middleware import no_cache_middleware, redirect_if_logged_in
from werkzeug.exceptions import RequestEntityTooLarge
from flask_babel import Babel, format_number
db = SQLAlchemy()
login_manager = LoginManager()

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

    # Import models after initializing extensions
    with app.app_context():
        from app.models import User
        db.create_all()  # Create database tables if they don't exist

    # Register Blueprints
    from app.views.admin import admin_bp
    from app.views.teacher import teacher_bp
    from app.views.student import student_bp
    from app.views.admin_categories import admin_categories_bp
    from app.views.teacher_courses import teacher_courses
    from app.views.course_lesson import course_lesson


    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_categories_bp)
    app.register_blueprint(teacher_courses)
    app.register_blueprint(course_lesson)

    # Home route
    @app.route('/')
    @redirect_if_logged_in
    def home():
        return render_template('home.html')


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
