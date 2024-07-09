# website/project.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Project, db
from website.forms import ProjectForm
from website import app

project_bp = Blueprint('project', __name__)