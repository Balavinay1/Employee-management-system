from flask import Flask
from config import Config
from .extensions import db, login_manager
from .models import User


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .auth import auth_bp
    from .main import main_bp
    from .employees import employees_bp
    from .attendance import attendance_bp
    from .leaves import leaves_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(leaves_bp, url_prefix='/leaves')

    @app.errorhandler(403)
    def forbidden(_error):
        from flask import render_template
        return render_template('403.html'), 403

    with app.app_context():
        db.create_all()

    return app
