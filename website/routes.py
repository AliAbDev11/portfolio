import secrets
from PIL import Image
import os
from website.models import User, Profile, db, Education, Experience, Service, Skill, Project, Contact
from flask import current_app, render_template, url_for, flash, redirect, request
from website.forms import RegistrationForm, LoginForm, UpdateProfileForm
from website import app, bcrypt
from sqlalchemy.orm import joinedload
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)
import logging

logging.basicConfig(level=logging.DEBUG)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_dir = os.path.join(current_app.root_path, 'static', 'images/user_pics')

    # Create the directory if it doesn't exist
    if not os.path.exists(picture_dir):
        os.makedirs(picture_dir)

    picture_path = os.path.join(picture_dir, picture_name)

    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_name

# Custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Home
@app.route("/")
@app.route("/home")
def home():
     # Query the education data
    if current_user.is_authenticated:
        user_id = current_user.id
        profiles = Profile.query.filter_by(user_id=current_user.id).all()
        experiences = Experience.query.filter_by(user_id=user_id).all()
        educations = Education.query.filter_by(user_id=user_id).all()
        services = Service.query.filter_by(user_id=user_id).all()
        skills = Skill.query.filter_by(user_id=user_id).all()
        projects = Project.query.filter_by(user_id=user_id).all()
    else:
        profiles = []
        experiences = []
        educations = []
        services = []
        skills = []
        projects = []
    return render_template("home.html", profiles=profiles, experiences=experiences, educations=educations, services=services, skills=skills, projects=projects )

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fullname=form.fullname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

# LogIn
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

# LogOut
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()

    if profile_form.validate_on_submit():
        # Handle profile picture upload
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.profile.image_file = picture_file

        # Update user and profile data
        current_user.fullname = profile_form.fullname.data
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.profile.phone_number = profile_form.phone_number.data
        current_user.profile.address = profile_form.address.data
        current_user.profile.bio_title = profile_form.bio_title.data
        current_user.profile.bio = profile_form.bio.data
        current_user.profile.github = profile_form.github.data
        current_user.profile.linkedin = profile_form.linkedin.data
        current_user.profile.twitter = profile_form.twitter.data
        current_user.profile.instagram = profile_form.instagram.data

        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating your profile: {str(e)}', 'danger')

    elif request.method == 'GET':
        # Populate form fields with current user data
        profile_form.fullname.data = current_user.fullname
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.phone_number.data = current_user.profile.phone_number
        profile_form.address.data = current_user.profile.address
        profile_form.bio_title.data = current_user.profile.bio_title
        profile_form.bio.data = current_user.profile.bio
        profile_form.github.data = current_user.profile.github
        profile_form.linkedin.data = current_user.profile.linkedin
        profile_form.twitter.data = current_user.profile.twitter
        profile_form.instagram.data = current_user.profile.instagram

    # Determine the image file path for rendering
    image_file = url_for("static", filename=f"images/user_pics/{current_user.profile.image_file}") if current_user.profile and current_user.profile.image_file else url_for("static", filename="images/user_pics/default.png")

    return render_template('admin/profile.html', title='Profile', image_file=image_file, profile_form=profile_form, active_tab="profile")