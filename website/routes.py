import secrets
from PIL import Image
import os
from website.models import User, Contact
from flask import render_template, url_for, flash, redirect, request
from website.forms import RegistrationForm, LoginForm, UpdateProfileForm
from website import app, bcrypt, db
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

workexperiences = [
    {
        "title": "Junior Developer",
        "company_name": "DevTech",
        "start_date": "2023",
        "start_end": "Current",
        "description": "As a Junior Developer at DevTech Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React. I collaborated with senior developers on API integrations and participated in code reviews and team meetings. Additionally, I implemented responsive design to ensure compatibility across various devices and assisted in troubleshooting and debugging tasks.",
    },
    {
        "title": "Junior Developer",
        "company_name": "TechDev",
        "start_date": "2022",
        "start_end": "2023",
        "description": "As a Junior Developer at TechDev Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React. I collaborated with senior developers on API integrations and participated in code reviews and team meetings. Additionally, I implemented responsive design to ensure compatibility across various devices and assisted in troubleshooting and debugging tasks.",
    },
]

educations = [
    {
        "degree": "Bachelors Degree",
        "school": "FST",
        "start_date": "2021",
        "start_end": "2022",
        "description": "As a Junior Developer at DevTech Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
    {
        "degree": "IT DEVELOPMENT DEGREE",
        "school": "ISTA",
        "start_date": "2019",
        "start_end": "2021",
        "description": "As a Junior Developer at TechDev Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
    {
        "degree": "HIGH SCHOOL DEGREE",
        "school": "Makkari",
        "start_date": "2021",
        "start_end": "2022",
        "description": "As a Junior Developer at TechDev Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
]

services = [
    {
        "image": "Bachelors Degree",
        "title": "Web Design",
        "description": "As a Junior Developer at DevTech Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
    {
        "image": "IT DEVELOPMENT DEGREE",
        "title": "Web Developent",
        "description": "As a Junior Developer at TechDev Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
    {
        "image": "HIGH SCHOOL DEGREE",
        "title": "UI/UX Design",
        "description": "As a Junior Developer at TechDev Technologies since June 2023, I have been involved in developing and maintaining web applications using HTML, CSS, JavaScript, and React.",
    },
]

skills = [
    {
        "title": "HTML",
        "percent": "92",
    },
    {
        "title": "CSS",
        "percent": "50",
    },
    {
        "title": "Design",
        "percent": "95",
    },
    {
        "title": "Python",
        "percent": "80",
    },
    {
        "title": "JavaScript",
        "percent": "92",
    },
    {
        "title": "Flask",
        "percent": "50",
    },
    {
        "title": "Django",
        "percent": "95",
    },
    {
        "title": "ReactJs",
        "percent": "80",
    },
]

portfolios = [
    {
        "image": "portfolio-7.jpg",
        "title": "Note WebApp",
        "description": "As a Junior Developer at DevTech Technologies since June 2023",
        "link": "https://github.com/AliAbDev11",
    },
    {
        "image": "portfolio-7.jpg",
        "title": "Blog Web App",
        "description": "As a Junior Developer at DevTech Technologies since June 2023",
        "link": "https://github.com/AliAbDev11",
    },
    {
        "image": "portfolio-7.jpg",
        "title": "Web Design",
        "description": "As a Junior Developer at DevTech Technologies since June 2023",
        "link": "https://github.com/AliAbDev11",
    },
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

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", profiles=profiles, workexperiences=workexperiences, educations=educations, services=services, skills=skills, portfolios=portfolios, links=links)

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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.fullname = profile_form.fullname.data
        current_user.phone_number = profile_form.phone_number.data
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio_title = profile_form.bio_title.data
        current_user.bio = profile_form.bio.data
        current_user.github = profile_form.github.data
        current_user.linkedin = profile_form.linkedin.data
        current_user.twitter = profile_form.twitter.data
        current_user.instagram = profile_form.instagram.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("profile"))  # Redirect to the same profile page
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"images/user_pics/{current_user.image_file}")
    return render_template(
        "admin/profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",  # Set active_tab to 'profile' when rendering profile.html
    )