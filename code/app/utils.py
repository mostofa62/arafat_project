from app import db
from app.models import User
from werkzeug.security import generate_password_hash
import logging
import os
# Set up basic logging to a file or console
logging.basicConfig(level=logging.INFO)

def create_admin_user():
    try:
        # Check if an admin user already exists
        admin_user = User.query.filter_by(role='admin').first()

        if not admin_user:
            # Define admin user credentials
            admin_email = 'admin@gmail.com'
            admin_name = 'admin'
            admin_password = 'admin123'  # Change this to any secure password

            # Hash the password before storing it
            hashed_password = generate_password_hash(admin_password)

            # Create the new admin user
            new_admin = User(name=admin_name, email=admin_email, password=hashed_password, role='admin')

            # Add and commit to the database
            db.session.add(new_admin)
            db.session.commit()

            # Log the created user credentials (only for development purposes)
            logging.info(f"Admin user created with email: {admin_email} and password: {admin_password}")
        else:
            logging.info("Admin user already exists.")
    
    except Exception as e:
        # Log any errors that occur during the process
        logging.error(f"Error while creating admin user: {e}")
        #raise  # Reraise the exception after logging it



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
