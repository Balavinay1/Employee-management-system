from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True, unique=True)

    employee = db.relationship('Employee', back_populates='user', foreign_keys=[employee_id])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    employees = db.relationship('Employee', back_populates='department', lazy=True)


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    designation = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False, default=0)
    joining_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default='Active')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    department = db.relationship('Department', back_populates='employees')
    user = db.relationship('User', back_populates='employee', uselist=False, foreign_keys=[User.employee_id])
    attendance_records = db.relationship('Attendance', back_populates='employee', cascade='all, delete-orphan')
    leaves = db.relationship('Leave', back_populates='employee', cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default='Present')
    check_in = db.Column(db.String(10))
    check_out = db.Column(db.String(10))

    employee = db.relationship('Employee', back_populates='attendance_records')

    __table_args__ = (
        db.UniqueConstraint('employee_id', 'attendance_date', name='uq_employee_attendance_date'),
    )


class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    applied_on = db.Column(db.Date, nullable=False, default=date.today)

    employee = db.relationship('Employee', back_populates='leaves')
