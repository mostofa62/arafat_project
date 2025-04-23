from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import Enrollment, Order, User, db, Course,Category
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware import redirect_if_logged_in, student_login_required
import os


from flask import Blueprint, render_template
from app.middleware import redirect_if_logged_in

checkout_bp = Blueprint('checkout_bp', __name__)

@checkout_bp.route('/<int:course_id>', methods=['GET', 'POST'])
@student_login_required
def checkout_course(course_id):
    course = Course.query.get_or_404(course_id)

    # Check if the current user has already purchased this course
    existing_order = Order.query.filter_by(student_id=current_user.id, course_id=course.id).first()
    # Check if already enrolled before inserting
    existing_enrollment = Enrollment.query.filter_by(student_id=current_user.id, course_id=course.id).first()

    if existing_order:
        #flash("You have already purchased this course.", "success")

        if not existing_enrollment:
            enrollment = Enrollment(
                student_id=current_user.id,
                course_id=course.id
            )
            db.session.add(enrollment)
            db.session.commit()

        #return redirect(url_for('student.dashboard'))  # or back to course page

    if request.method == 'POST':
        # Create a new order
        order = Order(
            student_id=current_user.id,
            course_id=course.id,
            amount=course.price,
            payment_status='completed'
        )
        db.session.add(order)
        enrollment = Enrollment(
            student_id=current_user.id,
            course_id=course.id
        )
        db.session.add(enrollment)
        db.session.commit()
        flash("Your purchase is completed!", "success")
        return redirect(url_for('checkout_bp.checkout_course', course_id=course_id))

    return render_template('checkout.html', course=course, existing_order=existing_order)
