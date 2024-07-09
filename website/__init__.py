from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from website.route_sections.experience import experience_bp
from website.route_sections.education import education_bp
from website.route_sections.service import service_bp
from website.route_sections.project import project_bp
from website.route_sections.skill import skill_bp

app.register_blueprint(experience_bp, url_prefix='/experience')
app.register_blueprint(education_bp, url_prefix='/education')
app.register_blueprint(service_bp, url_prefix='/service')
app.register_blueprint(skill_bp, url_prefix='/skill')
app.register_blueprint(project_bp, url_prefix='/project')

from website import routes