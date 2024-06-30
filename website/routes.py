import secrets
from PIL import Image
import os
from website.models import User
from flask import render_template
from website.forms import LoginForm
from website import app, bcrypt, db


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

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", profiles=profiles, workexperiences=workexperiences, educations=educations, services=services, skills=skills, portfolios=portfolios, links=links)

@app.route("/login")
def login():
    return render_template("admin/login.html")