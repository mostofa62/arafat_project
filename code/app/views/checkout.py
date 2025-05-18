from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, current_user, logout_user
from app.models import Enrollment, Order, User, db, Course,Category
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in, student_login_required
import os


from flask import Blueprint, render_template
from app.middleware import redirect_if_logged_in

checkout_bp = Blueprint('checkout_bp', __name__)

@checkout_bp.route('/', methods=['GET', 'POST'])
@student_login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('home_bp.home'))  # redirect to home or dashboard

    course_ids = [item['id'] for item in cart]

    existing_orders = Order.query.filter(
        Order.student_id == current_user.id,
        Order.course_id.in_(course_ids)
    ).all()
    existing_enrollments = Enrollment.query.filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id.in_(course_ids)
    ).all()

    owned_course_ids = set(order.course_id for order in existing_orders) | set(enroll.course_id for enroll in existing_enrollments)
    filtered_cart = [item for item in cart if item['id'] not in owned_course_ids]

    removed_count = len(cart) - len(filtered_cart)
    if removed_count > 0:
        session['cart'] = filtered_cart  # update session cart
        flash(f'{removed_count} course{"s" if removed_count > 1 else ""} were removed from your cart because you have already purchased and enrolled in {"them" if removed_count > 1 else "it"}.', 'warning')

    # If cart is empty after removing owned courses, redirect elsewhere
    if not filtered_cart:
        return redirect(url_for('checkout_bp.view_cart'))  # or dashboard, whatever suits you

    courses = Course.query.filter(Course.id.in_([item['id'] for item in filtered_cart])).all()
    total_price = sum(course.price for course in courses)

    if request.method == 'POST':
        for course in courses:
            existing_order = Order.query.filter_by(student_id=current_user.id, course_id=course.id).first()
            existing_enrollment = Enrollment.query.filter_by(student_id=current_user.id, course_id=course.id).first()

            if existing_order:
                if not existing_enrollment:
                    enrollment = Enrollment(student_id=current_user.id, course_id=course.id)
                    db.session.add(enrollment)
            else:
                new_order = Order(
                    student_id=current_user.id,
                    course_id=course.id,
                    amount=course.price,
                    payment_status='completed'
                )
                db.session.add(new_order)
                enrollment = Enrollment(student_id=current_user.id, course_id=course.id)
                db.session.add(enrollment)

        db.session.commit()
        session.pop('cart', None)

        # After successfully creating orders and enrollments
        order_course_ids = [course.id for course in courses]  # courses were just ordered
        session['recent_order_course_ids'] = order_course_ids
        
        flash("Your order has been placed and enrollments updated.", "success")
        return redirect(url_for('checkout_bp.order_complete'))

    return render_template('checkout.html', cart=filtered_cart, total_price=total_price)

@checkout_bp.route('/complete')
@student_login_required
def order_complete():
    course_ids = session.get('recent_order_course_ids')

    if not course_ids:
        flash("No recent order information found.", "warning")
        return redirect(url_for('home_bp.home'))

    courses = Course.query.filter(Course.id.in_(course_ids)).all()

    # Calculate total bill
    total_price = sum(course.price for course in courses)

    # Clear the session data so it doesn't show again on refresh
    session.pop('recent_order_course_ids', None)

    return render_template('order_complete.html', courses=courses, total_price=total_price)



@checkout_bp.route('/cart/add/<int:course_id>', methods=['POST'])
def add_to_cart(course_id):
    if current_user.is_authenticated:
        course = Course.query.get_or_404(course_id)

        # Check if the user has already purchased the course
        existing_order = Order.query.filter_by(student_id=current_user.id, course_id=course.id).first()
        existing_enrollment = Enrollment.query.filter_by(student_id=current_user.id, course_id=course.id).first()

        if existing_order or existing_enrollment:
            flash("You have already purchased or enrolled in this course.", "warning")
            return redirect(request.referrer or url_for('home_bp.all_courses'))

    # Get the current cart or initialize a new one
    cart = session.get('cart', [])

    # Check if course is already in cart
    for item in cart:
        if item['id'] == course_id:
            flash('Course is already in your cart.', 'info')
            return redirect(request.referrer or url_for('home'))

    # Fetch course details from DB
    course = Course.query.get_or_404(course_id)

    # Add course to cart with details
    cart.append({
        'id': course.id,
        'title': course.title,
        'price': float(course.price),  # Ensure JSON serializable
        'thumbnail': course.thumbnail
    })

    session['cart'] = cart
    flash('Course added to cart successfully!', 'success')
    return redirect(request.referrer or url_for('home'))




@checkout_bp.route('/cart/list')
def view_cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)



@checkout_bp.route('/cart/remove/<int:course_id>', methods=['POST'])
def remove_from_cart(course_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['id'] != course_id]

    session['cart'] = updated_cart
    flash('Course removed from cart.', 'info')
    return redirect(request.referrer or url_for('view_cart'))

