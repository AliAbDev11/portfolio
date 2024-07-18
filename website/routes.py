import secrets
from PIL import Image
import os
from website.models import User, Profile, db, Education, Experience, Service, Skill, Project, Contact
from flask import render_template, url_for, flash, redirect, request
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


profiles = [
    {
        "fullname": "Ali Ait Brahim",
        "phone": "+212 696813151",
        "jobs": "Web Developer / Web desiner",
        "email": "aliaitbrahim@gmail.com",
        "address": "RES FERDAOUS, OULFA, CASABLANCA, MOROCCO",
        "image": "LogoAB.png",
        "about_title": "Hello there!",
        "about_description": "Skilled Web Developer with over 1 year of experience in creating websites and web applications. Proficient in front-end and back-end programming languages, as well as modern frameworks and tools. Passionate about web development and constantly keeping up with the latest technological trends. Demonstrated experience in designing, developing, testing, and deploying high-performance and user-friendly websites. Ability to work in a team, solve problems effectively, and meet deadlines. Additionally, I am a talented Web Designer and UI/UX Designer, combining technical proficiency with a keen eye for design to create visually appealing and user-centric digital experiences.",
    }
]

links = [
    {
        "github": "https://github.com/AliAbDev11",
        "linkedin": "https://www.linkedin.com/in/ali-ait-brahim-51653b201/",
        "instagram": "https://www.instagram.com/ali_ab_harry/",
        "twitter": "https://x.com/AliAitBrahim11",
    },
]

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
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
        # profiles = Profile.query.filter_by(user_id=user_id).all()
        experiences = Experience.query.filter_by(user_id=user_id).all()
        educations = Education.query.filter_by(user_id=user_id).all()
        services = Service.query.filter_by(user_id=user_id).all()
        skills = Skill.query.filter_by(user_id=user_id).all()
        projects = Project.query.filter_by(user_id=user_id).all()
    else:
        # profiles = []
        experiences = []
        educations = []
        services = []
        skills = []
        projects = []
    return render_template("home.html", profiles=profiles, experiences=experiences, educations=educations, services=services, skills=skills, projects=projects, links=links)

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

    # Fetch current_user from Flask-Login
    user_id = current_user.id
    current_user_obj = User.query.options(joinedload(User.profile)).filter_by(id=user_id).first()

    if profile_form.validate_on_submit():
        # Handle form submission and update database
        if not current_user_obj.profile:
            # If profile doesn't exist, create a new one
            new_profile = Profile(
                user_id=user_id,
                phone_number=profile_form.phone_number.data,
                bio_title=profile_form.bio_title.data,
                bio=profile_form.bio.data,
                github=profile_form.github.data,
                linkedin=profile_form.linkedin.data,
                twitter=profile_form.twitter.data,
                instagram=profile_form.instagram.data
            )
            db.session.add(new_profile)
        else:
            # If profile exists, update it
            current_user_obj.profile.phone_number = profile_form.phone_number.data
            current_user_obj.profile.bio_title = profile_form.bio_title.data
            current_user_obj.profile.bio = profile_form.bio.data
            current_user_obj.profile.github = profile_form.github.data
            current_user_obj.profile.linkedin = profile_form.linkedin.data
            current_user_obj.profile.twitter = profile_form.twitter.data
            current_user_obj.profile.instagram = profile_form.instagram.data

        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        # Populate form fields with data from models
        if current_user_obj:
            profile_form.fullname.data = current_user_obj.fullname
            profile_form.email.data = current_user_obj.email
            profile_form.username.data = current_user_obj.username

            if current_user_obj.profile:
                profile_form.phone_number.data = current_user_obj.profile.phone_number
                profile_form.bio_title.data = current_user_obj.profile.bio_title
                profile_form.bio.data = current_user_obj.profile.bio
                profile_form.github.data = current_user_obj.profile.github
                profile_form.linkedin.data = current_user_obj.profile.linkedin
                profile_form.twitter.data = current_user_obj.profile.twitter
                profile_form.instagram.data = current_user_obj.profile.instagram

    # Determine the image file path for rendering
    image_file = url_for("static", filename=f"images/user_pics/{current_user_obj.profile.image_file}") if current_user_obj.profile and current_user_obj.profile.image_file else url_for("static", filename="images/user_pics/default.png")

    return render_template(
        "admin/profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile"
    )