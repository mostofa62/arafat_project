from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from app import db
from app.models import Category
from app.forms import CategoryForm
from werkzeug.utils import secure_filename
import os
from  datetime import datetime

admin_categories_bp = Blueprint('admin_categories', __name__, url_prefix='/admin/categories')

@admin_categories_bp.route('/')
@login_required
def index():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('admin/categories/index.html', categories=categories, title='Categories')

@admin_categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        # Now save the thumbnail with the cat ID
        if form.thumbnail.data:
            thumbnail_filename = save_thumbnail(category.id, form.thumbnail.data)
            category.thumbnail = thumbnail_filename
            db.session.commit()  # Update the cat with the thumbnail filename
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin_categories.index'))
    return render_template('admin/categories/create.html', form=form, title='Create Category')

@admin_categories_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        try:
            if form.thumbnail.data:
                # If the category already has a thumbnail, delete the old one
                if category.thumbnail:
                    old_thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cat_thumb', category.thumbnail)
                    if os.path.exists(old_thumbnail_path):
                        os.remove(old_thumbnail_path)

                # Save the new thumbnail and update the category record
                thumbnail_filename = save_thumbnail(category.id, form.thumbnail.data)
                category.thumbnail = thumbnail_filename
            category.name = form.name.data
            category.updated_at = datetime.now()
            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin_categories.index'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('admin/categories/edit.html', form=form, category=category, title='Edit Category')

@admin_categories_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories.index'))







# Helper function to save thumbnail with validation
def save_thumbnail(category_id, file):
    if file:
        # Allowed extensions
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        max_file_size = current_app.config['THUMB_CONTENT_LENGTH']

        ALLOWED_EXTENSIONS_STR = ', '.join(allowed_extensions)

        # Check file extension
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_extension not in allowed_extensions:
            raise ValueError(f'Invalid file extension. Allowed extensions are: {ALLOWED_EXTENSIONS_STR}')

        # Check file size
        file.seek(0, os.SEEK_END)  # Move to the end of the file to get its size
        file_size = file.tell()  # Get the current position (file size in bytes)
        file.seek(0)  # Reset file pointer to the beginning
        if file_size > max_file_size:
            raise ValueError('File size exceeds the 1MB limit')

        # Generate the filename using the cat ID and original file name
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{category_id}_{filename}"

        # Save the file
        cat_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cat_thumb')
        filepath = os.path.join(cat_dir, new_filename)
        os.makedirs(cat_dir, exist_ok=True)
        file.save(filepath)
        return new_filename

    return None
