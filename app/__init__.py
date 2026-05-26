from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.student_route import student_bp
    from app.routes.course_route import course_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    return app
