import pytest
from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret',
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username='admin', role='admin')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Employee Management System' in response.data


def test_login(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data
