from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .decorators import roles_required
from .extensions import db
from .models import Employee, Leave

leaves_bp = Blueprint('leaves', __name__)


@leaves_bp.route('/')
@login_required
def list_leaves():
    status = request.args.get('status', '').strip()
    query = Leave.query.join(Employee)

    if current_user.role == 'employee':
        query = query.filter(Leave.employee_id == current_user.employee_id)
    elif status:
        query = query.filter(Leave.status == status)

    records = query.order_by(Leave.applied_on.desc()).all()
    return render_template('leaves/list.html', records=records, selected_status=status)


@leaves_bp.route('/new', methods=['GET', 'POST'])
@login_required
@roles_required('hr', 'employee')
def create_leave():
    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()
    if request.method == 'POST':
        employee_id = current_user.employee_id if current_user.role == 'employee' else request.form.get('employee_id')
        try:
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        except (TypeError, ValueError):
            flash('Please provide valid start and end dates.', 'danger')
            return render_template('leaves/form.html', employees=employees)

        if not employee_id or start_date > end_date:
            flash('Please select an employee and use a valid date range.', 'danger')
            return render_template('leaves/form.html', employees=employees)

        record = Leave(
            employee_id=int(employee_id),
            leave_type=request.form.get('leave_type', 'Casual'),
            start_date=start_date,
            end_date=end_date,
            reason=request.form.get('reason', '').strip(),
            status='Pending',
        )
        if not record.reason:
            flash('Reason is required.', 'danger')
            return render_template('leaves/form.html', employees=employees)

        db.session.add(record)
        db.session.commit()
        flash('Leave request submitted.', 'success')
        return redirect(url_for('leaves.list_leaves'))

    return render_template('leaves/form.html', employees=employees)


@leaves_bp.route('/<int:leave_id>/status', methods=['POST'])
@login_required
@roles_required('admin', 'hr')
def update_leave_status(leave_id):
    record = Leave.query.get_or_404(leave_id)
    new_status = request.form.get('status')
    if new_status not in {'Approved', 'Rejected', 'Pending'}:
        flash('Invalid leave status.', 'danger')
    else:
        record.status = new_status
        db.session.commit()
        flash(f'Leave marked as {new_status}.', 'success')
    return redirect(url_for('leaves.list_leaves'))
