from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in

student_bp = Blueprint('student', __name__)

@student_bp.route('/register', methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please login.', 'error')
            return redirect(url_for('student.login'))
        
        # Create new student user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role='student')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('student.login'))
    
    return render_template('student/register.html', user_type='student', title='Student Registration')

@student_bp.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'POST':
        next_page = request.form.get('next')
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role='student').first()
        if user and check_password_hash(user.password, password):
            login_user(user)            
            print('next_page',type(next_page))
            if next_page!= "None":
                return redirect(next_page)
            else:
               return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    next_page = request.args.get('next')
    return render_template('student/login.html', user_type='student', title='Student Login',next=next_page)
@student_bp.route('/')
@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student/dashboard.html', title_enrollment = 'Your Enrollments')

@student_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('student.login'))

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    return render_template('student/profile.html')

@student_bp.route('/update-password', methods=['GET', 'POST'])
@login_required
def update_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if check_password_hash(current_user.password, current_password):
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        else:
            flash('Current password is incorrect.', 'error')
    return render_template('student/update_password.html')




@student_bp.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)

        # Get the new email and check if it is unique
        new_email = request.form['email']
        if User.query.filter_by(email=new_email).first() and new_email != user.email:
            flash('Email is already in use!', 'error')
            return redirect(url_for('student.update_profile'))

        # Update the user data
        user.email = new_email
        user.bio = request.form.get('bio', '')  # Optional bio for teacher/student

        # Update password if provided
        password = request.form.get('password')
        if password:
            user.password = generate_password_hash(password)  # Assuming you are using Flask's Werkzeug for hashing passwords

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.update_profile'))

    return render_template('common/update_profile.html', user=current_user, title='Student Profile')
