import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from app.utils import create_admin_user
from babel.numbers import format_currency
from datetime import datetime
app = create_app()

@app.template_filter('format_currency')
def format_currency_filter(value, currency='USD', locale='en_US'):
    return format_currency(value, currency, locale=locale)
# Context processor to inject the default title
@app.context_processor
def inject_title():
    return {
        'default_title': os.getenv('app_name', 'Default App Name'),
        'current_year':datetime.now().year
    }

# Check and create admin user if not already present
with app.app_context():
    # Create all tables
    db.create_all()

    # Check if the admin user exists
    create_admin_user()
   

if __name__ == '__main__':
    app.run(debug=True)
