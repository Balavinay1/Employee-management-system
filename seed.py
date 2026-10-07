from app import create_app
from app.extensions import db
from app.models import Department, Employee, User

app = create_app()

with app.app_context():
    if User.query.filter_by(username='admin').first():
        print('Seed data already exists.')
        raise SystemExit

    it = Department(name='IT', description='Technology and software development')
    hr = Department(name='Human Resources', description='People operations and recruitment')
    sales = Department(name='Sales', description='Sales and business development')
    db.session.add_all([it, hr, sales])
    db.session.flush()

    employee = Employee(
        employee_code='EMP001', first_name='Rahul', last_name='Sharma',
        email='rahul@example.com', phone='9876543210', designation='Python Developer',
        salary=500000, department_id=it.id, status='Active'
    )
    db.session.add(employee)
    db.session.flush()

    admin = User(username='admin', role='admin')
    admin.set_password('Admin@123')
    hr_user = User(username='hr', role='hr')
    hr_user.set_password('Hr@123')
    employee_user = User(username='rahul', role='employee', employee_id=employee.id)
    employee_user.set_password('Employee@123')
    db.session.add_all([admin, hr_user, employee_user])
    db.session.commit()

    print('Seed complete.')
    print('Admin    : admin / Admin@123')
    print('HR       : hr / Hr@123')
    print('Employee : rahul / Employee@123')
