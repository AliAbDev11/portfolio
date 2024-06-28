import secrets
from PIL import Image
import os
from website.models import User
from flask import render_template
from website.forms import LoginForm
from website import app, bcrypt, db
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")