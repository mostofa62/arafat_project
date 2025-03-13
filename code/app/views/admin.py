from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in
import os
import uuid
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role='admin').first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin/login.html', user_type='admin',title='Admin Login')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    users = User.query.all()  # Example: Admin can view all users
    return render_template('admin/dashboard.html', users=users, title='My Dashboard')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    return render_template('admin/profile.html')

@admin_bp.route('/update-password', methods=['GET', 'POST'])
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
    return render_template('admin/update_password.html')




# General User List with Pagination
@admin_bp.route('/users', methods=['GET'])
@login_required
def user_list():    
    return render_template('admin/user_list.html', title='User List')


@admin_bp.route('/user-data', methods=['GET'])
@admin_bp.route('/user-data/<string:role>', methods=['GET'])
def user_data(role=None):
    # Get DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', '').strip()

    # Query users
    query = User.query

    # Apply search filter if provided
    if search_value:
        query = query.filter(
            (User.name.ilike(f"%{search_value}%")) |
            (User.email.ilike(f"%{search_value}%")) |
            (User.role.ilike(f"%{search_value}%"))
        )

    # Apply role filter if provided (optional parameter)
    if role:
        query = query.filter(User.role == role)

    # Count total and filtered results
    total_records = query.count()
    users = query.offset(start).limit(length).all()

    # Serialize data for DataTables
    data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            #"status": user.status
        }
        for user in users
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data
    })

# Teacher List with Pagination
@admin_bp.route('/teachers', methods=['GET'])
@login_required
def teacher_list():    
    return render_template('admin/teacher_list.html',role='teacher', title='Teacher List')

# Student List with Pagination
@admin_bp.route('/students', methods=['GET'])
@login_required
def student_list():   
    return render_template('admin/student_list.html',role='student', title='Student List')

# Admin List with Pagination
@admin_bp.route('/admins', methods=['GET'])
@login_required
def admin_list():      
    return render_template('admin/admin_list.html',role='admin', title='Admin List')



from app.utils import allowed_file

@admin_bp.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    try:
        # Validate the required fields
        chunk = request.files.get('file')
        total_chunks = request.form.get('total_chunks', type=int)
        chunk_index = request.form.get('chunk_index', type=int)
        file_id = request.form.get('file_id') or uuid.uuid4().hex
        filename = request.form.get('filename')

        if not chunk or not filename or total_chunks is None or chunk_index is None:
            return jsonify({"error": "Invalid request parameters"}), 400

        # Validate the file type
        if not allowed_file(filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Validate the chunk size
        max_chunk_size = current_app.config['MAX_CONTENT_LENGTH']  # 2 MB
        if chunk.content_length > max_chunk_size:
            return jsonify({"error": "Chunk size exceeds 2 MB"}), 413

        # Temporary storage path
        temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', file_id)
        os.makedirs(temp_dir, exist_ok=True)

        # Save the chunk
        chunk_path = os.path.join(temp_dir, f"chunk_{chunk_index}")
        chunk.save(chunk_path)

        # If all chunks are received, assemble the file
        if chunk_index + 1 == total_chunks:
            final_filename = f"{uuid.uuid4().hex}_{secure_filename(filename)}"
            final_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], final_filename)
            with open(final_filepath, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(temp_dir, f"chunk_{i}")
                    with open(chunk_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

            # Clean up temporary chunks
            for i in range(total_chunks):
                os.remove(os.path.join(temp_dir, f"chunk_{i}"))
            os.rmdir(temp_dir)

            #save to user , remove this code for any other project to reuseable case
            user = User.query.get(current_user.id)
            if user:
                # Check if the user already has a profile picture
                if user.profile_picture:
                    # Store the old profile picture in a temp variable
                    old_profile_picture = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile_picture)
                    
                    # Check if the file exists and remove it
                    if os.path.exists(old_profile_picture):
                        os.remove(old_profile_picture)

                # Update the user's profile picture with the new file
                user.profile_picture = final_filename
                db.session.commit()

            #end save to user

            #return jsonify({"filepath": f"static/uploads/{final_filename}"}), 200
            return jsonify({
                "filepath": f"static/uploads/{final_filename}", 
                "filename": final_filename,
                "image_url": url_for('static', filename=f'uploads/{final_filename}')
                }), 200

        return jsonify({"message": "Chunk uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@admin_bp.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)

        # Get the new email and check if it is unique
        new_email = request.form['email']
        if User.query.filter_by(email=new_email).first() and new_email != user.email:
            flash('Email is already in use!', 'error')
            return redirect(url_for('admin.update_profile'))

        # Update the user data
        user.email = new_email
        user.bio = request.form.get('bio', '')  # Optional bio for teacher/student

        # Only update the profile picture if a new one is provided
        # new_profile_picture = request.form.get('profile_picture')
        # if new_profile_picture:
        #     user.profile_picture = new_profile_picture  # Update with new profile picture
        # If no new profile picture is provided, retain the existing one
        # user.profile_picture will remain unchanged

        # Update password if provided
        password = request.form.get('password')
        if password:
            user.password = generate_password_hash(password)  # Assuming you are using Flask's Werkzeug for hashing passwords

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.update_profile'))

    return render_template('common/update_profile.html', user=current_user, title='Admin Profile')