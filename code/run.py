from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from app.utils import create_admin_user

app = create_app()

# Context processor to inject the default title
@app.context_processor
def inject_title():
    return {'default_title': 'Tutorial Portal'}

# Check and create admin user if not already present
with app.app_context():
    # Create all tables
    db.create_all()

    # Check if the admin user exists
    create_admin_user()
   

if __name__ == '__main__':
    app.run(debug=True)
