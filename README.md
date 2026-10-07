# Employee Management System — Python Fresher Project

A portfolio-ready employee management application built with **Python, Flask, SQLAlchemy and SQLite/MySQL**.

## Features

- User login/logout
- Password hashing
- Role-based access: Admin, HR, Employee
- Employee registration and CRUD
- Employee search and filtering
- Department management through relational database design
- Attendance recording and filtering
- Leave application and approval/rejection workflow
- Dashboard statistics
- Form validation and duplicate checks
- Automated tests with pytest
- SQLite for zero-configuration local development
- MySQL-ready configuration

## Tech Stack

- Python 3.10+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLAlchemy ORM
- SQLite (default) / MySQL
- HTML/CSS/Jinja2
- pytest

## Project Structure

```text
employee_management_system/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── decorators.py
│   ├── auth.py
│   ├── main.py
│   ├── employees.py
│   ├── attendance.py
│   ├── leaves.py
│   ├── static/style.css
│   └── templates/
├── tests/test_app.py
├── config.py
├── run.py
├── seed.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## 1. Install

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Create demo data

```bash
python seed.py
```

Demo accounts:

| Role | Username | Password |
|---|---|---|
| Admin | admin | Admin@123 |
| HR | hr | Hr@123 |
| Employee | rahul | Employee@123 |

Change these passwords before using the project outside a demo environment.

## 3. Run

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

## MySQL setup (optional)

Create a database:

```sql
CREATE DATABASE employee_management;
```

Set the environment variable:

```text
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/employee_management
```

Then run:

```bash
python seed.py
python run.py
```

## Run tests

```bash
pytest
```

