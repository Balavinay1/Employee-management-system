from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_
from .decorators import roles_required
from .extensions import db
from .models import Department, Employee, User

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/')
@login_required
def list_employees():
    q = request.args.get('q', '').strip()
    department_id = request.args.get('department_id', type=int)
    status = request.args.get('status', '').strip()

    query = Employee.query
    if q:
        like = f'%{q}%'
        query = query.filter(or_(Employee.first_name.ilike(like), Employee.last_name.ilike(like),
                                 Employee.employee_code.ilike(like), Employee.email.ilike(like),
                                 Employee.designation.ilike(like)))
    if department_id:
        query = query.filter_by(department_id=department_id)
    if status:
        query = query.filter_by(status=status)

    employees = query.order_by(Employee.id.desc()).all()
    departments = Department.query.order_by(Department.name).all()
    return render_template('employees/list.html', employees=employees, departments=departments,
                           q=q, selected_department=department_id, selected_status=status)


@employees_bp.route('/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'hr')
def create_employee():
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        employee = build_employee_from_form()
        if not validate_employee(employee):
            return render_template('employees/form.html', employee=employee, departments=departments, title='Add Employee')
        db.session.add(employee)
        db.session.commit()
        flash('Employee created successfully.', 'success')
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/form.html', employee=None, departments=departments, title='Add Employee')


@employees_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'hr')
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        update_employee_from_form(employee)
        if not validate_employee(employee, current_id=employee.id):
            return render_template('employees/form.html', employee=employee, departments=departments, title='Edit Employee')
        db.session.commit()
        flash('Employee updated successfully.', 'success')
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/form.html', employee=employee, departments=departments, title='Edit Employee')


@employees_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@roles_required('admin')
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if employee.user:
        db.session.delete(employee.user)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully.', 'success')
    return redirect(url_for('employees.list_employees'))


def build_employee_from_form():
    employee = Employee(
        employee_code=request.form.get('employee_code', '').strip(),
        first_name=request.form.get('first_name', '').strip(),
        last_name=request.form.get('last_name', '').strip(),
        email=request.form.get('email', '').strip().lower(),
        phone=request.form.get('phone', '').strip(),
        designation=request.form.get('designation', '').strip(),
        salary=float(request.form.get('salary') or 0),
        status=request.form.get('status', 'Active'),
        department_id=int(request.form.get('department_id')),
    )
    joining_date = request.form.get('joining_date')
    employee.joining_date = datetime.strptime(joining_date, '%Y-%m-%d').date() if joining_date else datetime.today().date()
    return employee


def update_employee_from_form(employee):
    employee.employee_code = request.form.get('employee_code', '').strip()
    employee.first_name = request.form.get('first_name', '').strip()
    employee.last_name = request.form.get('last_name', '').strip()
    employee.email = request.form.get('email', '').strip().lower()
    employee.phone = request.form.get('phone', '').strip()
    employee.designation = request.form.get('designation', '').strip()
    employee.salary = float(request.form.get('salary') or 0)
    employee.status = request.form.get('status', 'Active')
    employee.department_id = int(request.form.get('department_id'))
    joining_date = request.form.get('joining_date')
    employee.joining_date = datetime.strptime(joining_date, '%Y-%m-%d').date() if joining_date else employee.joining_date


def validate_employee(employee, current_id=None):
    if not all([employee.employee_code, employee.first_name, employee.last_name, employee.email, employee.designation]):
        flash('Please fill all required fields.', 'danger')
        return False
    if employee.salary < 0:
        flash('Salary cannot be negative.', 'danger')
        return False
    code_exists = Employee.query.filter_by(employee_code=employee.employee_code).first()
    email_exists = Employee.query.filter_by(email=employee.email).first()
    if code_exists and code_exists.id != current_id:
        flash('Employee code already exists.', 'danger')
        return False
    if email_exists and email_exists.id != current_id:
        flash('Email already exists.', 'danger')
        return False
    return True
