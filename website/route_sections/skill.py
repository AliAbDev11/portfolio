# website/skill.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Skill, db
from website.forms import SkillForm
from website import app

skill_bp = Blueprint('skill', __name__)