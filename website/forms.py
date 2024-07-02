from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)

from website.models import User, Profile, Contact

class RegistrationForm(FlaskForm):
    fullname = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            # Regexp(
            #     message="Password must be 8-32 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&_)"

            # ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please chosse a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please chosse a different one")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class ContactForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send Message')

# Update Profile
class UpdateProfileForm(FlaskForm):
    fullname = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=25)]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(),
        Length(min=10, max=15, message='Phone number must be between 10 and 15 characters.'),
        Regexp(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+212 96813151'. Up to 15 digits allowed.")
    ])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    bio_title = StringField("About Title", validators=[DataRequired(), Length(min=4, max=20)])
    bio = TextAreaField("About Me",validators=[DataRequired()])
    github = StringField("Github", validators=[DataRequired()])
    linkedin = StringField("Linkedin", validators=[DataRequired()])
    twitter = StringField("Twitter")
    instagram = StringField("Instagram")
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Profile.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please chosse a different one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Profile.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please chosse a different one"
                )
    
    def validate_phone_number(self, phone_number):
        existing_user = Profile.query.filter_by(phone_number=phone_number.data).first()
        if existing_user:
            raise ValidationError('That phone number is already taken. Please choose a different one.')