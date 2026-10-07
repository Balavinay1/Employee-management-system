from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .decorators import roles_required
from .extensions import db
from .models import Attendance, Employee

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/')
@login_required
def list_attendance():
    employee_id = request.args.get('employee_id', type=int)
    attendance_date = request.args.get('attendance_date', '').strip()

    query = Attendance.query.join(Employee)
    if current_user.role == 'employee':
        if not current_user.employee_id:
            records = []
        else:
            query = query.filter(Attendance.employee_id == current_user.employee_id)
            records = query.order_by(Attendance.attendance_date.desc()).all()
    else:
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        if attendance_date:
            try:
                query = query.filter(Attendance.attendance_date == datetime.strptime(attendance_date, '%Y-%m-%d').date())
            except ValueError:
                flash('Invalid date format.', 'danger')
        records = query.order_by(Attendance.attendance_date.desc()).all()

    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()
    return render_template('attendance/list.html', records=records, employees=employees,
                           selected_employee=employee_id, selected_date=attendance_date)


@attendance_bp.route('/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'hr')
def create_attendance():
    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()
    if request.method == 'POST':
        try:
            employee_id = int(request.form.get('employee_id'))
            attendance_date = datetime.strptime(request.form.get('attendance_date'), '%Y-%m-%d').date()
        except (TypeError, ValueError):
            flash('Please provide a valid employee and date.', 'danger')
            return render_template('attendance/form.html', employees=employees)

        existing = Attendance.query.filter_by(employee_id=employee_id, attendance_date=attendance_date).first()
        if existing:
            flash('Attendance for this employee and date already exists.', 'danger')
            return render_template('attendance/form.html', employees=employees)

        record = Attendance(
            employee_id=employee_id,
            attendance_date=attendance_date,
            status=request.form.get('status', 'Present'),
            check_in=request.form.get('check_in', '').strip(),
            check_out=request.form.get('check_out', '').strip(),
        )
        db.session.add(record)
        db.session.commit()
        flash('Attendance recorded.', 'success')
        return redirect(url_for('attendance.list_attendance'))

    return render_template('attendance/form.html', employees=employees)


@attendance_bp.route('/<int:attendance_id>/delete', methods=['POST'])
@login_required
@roles_required('admin', 'hr')
def delete_attendance(attendance_id):
    record = Attendance.query.get_or_404(attendance_id)
    db.session.delete(record)
    db.session.commit()
    flash('Attendance record deleted.', 'success')
    return redirect(url_for('attendance.list_attendance'))
