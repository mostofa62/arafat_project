from flask_login import UserMixin
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'teacher', 'student'
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<User {self.name}>"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    thumbnail = db.Column(db.Text)

     # Relationship with Course
    courses = db.relationship('Course', back_populates='category', lazy='dynamic')



class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'))
    thumbnail = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # Relationship with Category
    category = db.relationship('Category', back_populates='courses')
    # Relationship with lessons
    lessons = db.relationship('Lesson', back_populates='course', cascade='all, delete-orphan', lazy='dynamic')
    teacher = db.relationship('User', backref='courses', foreign_keys=[teacher_id])


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'video', 'pdf', or 'text'
    content_url = db.Column(db.Text)  # For video/pdf URL
    text_content = db.Column(db.Text)  # For text-based lessons
    duration = db.Column(db.Interval)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    course = db.relationship('Course', back_populates='lessons')



class CourseProgress(db.Model):
    __tablename__ = 'course_progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.now())

    student = db.relationship('User', backref='course_progress')
    course = db.relationship('Course', backref='course_progress')
    lesson = db.relationship('Lesson', backref='course_progress')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.now())

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)

    student = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now())

    student = db.relationship('User', backref='orders')
    course = db.relationship('Course', backref='orders')


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    course = db.relationship('Course', backref=db.backref('quizzes', cascade='all, delete-orphan'))
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', cascade='all, delete-orphan')


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    answers = db.relationship('Answer', backref='question', cascade='all, delete-orphan')
    attempt_answers = db.relationship('AttemptAnswer', backref='question', cascade='all, delete-orphan')


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=True)
    attempted_at = db.Column(db.DateTime, default=datetime.now)

    student = db.relationship('User', backref=db.backref('quiz_attempts', cascade='all, delete-orphan'))
    attempt_answers = db.relationship('AttemptAnswer', backref='attempt', cascade='all, delete-orphan')


class AttemptAnswer(db.Model):
    __tablename__ = 'attempt_answers'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    selected_answer_id = db.Column(db.Integer, db.ForeignKey('answers.id', ondelete='CASCADE'), nullable=False)

    selected_answer = db.relationship('Answer')