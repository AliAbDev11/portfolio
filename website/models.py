from datetime import datetime
from website import db, login_manager
from flask_login import UserMixin

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


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Contact('{self.fullname}', '{self.email}', '{self.subject}', '{self.date_submitted}')"

