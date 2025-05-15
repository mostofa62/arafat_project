from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from app import db
from app.models import Course
import os
from  datetime import datetime

admin_courses_bp = Blueprint('admin_courses', __name__, url_prefix='/admin/courses')