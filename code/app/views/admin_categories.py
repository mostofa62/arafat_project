from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Category
from app.forms import CategoryForm

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
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin_categories.index'))
    return render_template('admin/categories/create.html', form=form, title='Create Category')

@admin_categories_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.updated_at = db.func.current_timestamp()
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories.index'))
    return render_template('admin/categories/edit.html', form=form, category=category, title='Edit Category')

@admin_categories_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories.index'))
