from flask import Blueprint, render_template
from flask_login import login_required
from .extensions import db
from .models import Employee, Department, Attendance, Leave

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        employee_count=Employee.query.count(),
        department_count=Department.query.count(),
        present_count=Attendance.query.filter_by(status='Present').count(),
        pending_leaves=Leave.query.filter_by(status='Pending').count(),
    )
