from datetime import datetime
from website import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)
    experiences = db.relationship('Experience', backref='author', lazy=True)
    educations = db.relationship('Education', backref='author', lazy=True)
    services = db.relationship('Service', backref='author', lazy=True)
    skills = db.relationship('Skill', backref='author', lazy=True)
    projects = db.relationship('Project', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        try:
            user_id = s.loads(token, max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<User {self.username}>"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    bio_title = db.Column(db.String(25), nullable=False)
    bio = db.Column(db.Text, nullable=True, default="")
    github = db.Column(db.String(100), nullable=False)
    linkedin = db.Column(db.String(100), nullable=False)
    twitter = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Profile {self.user.username}>"

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Experience('{self.job_title}', '{self.company_name}', '{self.start_date}', '{self.end_date}', '{self.is_current}')"
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(50), nullable=False)
    school = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Education('{self.degree}', '{self.school}', '{self.start_date}', '{self.end_date}', '{self.is_current}')"
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(20))
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Service('{self.title}', '{self.description}')"
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    percent = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Skill('{self.title}', '{self.percent}')"
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(20))  # Adjust size and type as necessary
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Project('{self.title}', '{self.description}', '{self.link}')"


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Contact('{self.fullname}', '{self.email}', '{self.subject}', '{self.date_submitted}')"

