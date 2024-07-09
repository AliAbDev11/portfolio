# website/skill.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Skill, db
from website.forms import SkillForm
from website import app

skill_bp = Blueprint('skill', __name__)

@app.route('/dashboard/list_skills', methods=['GET'])
@login_required
def skill():
    user_id = current_user.id
    degree = request.args.get('degree', '')
    school = request.args.get('school', '')

    query = Skill.query.filter_by(user_id=user_id)

    if degree:
        query = query.filter(Skill.degree.ilike(f'%{degree}%'))
    if school:
        query = query.filter(Skill.school.ilike(f'%{school}%'))

    skills = query.all()

    return render_template('admin/Skills/list_skills.html', skills=skills)

@app.route('/dashboard/add_skill', methods=["GET", "POST"])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        new_skill = Skill(
            title=form.title.data,
            percent=form.percent.data,
            user_id=current_user.id
        )
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill added successfully', 'success')
        return redirect(url_for('skill'))
    return render_template('admin/Skills/add_skill.html', form=form)

@app.route('/dashboard/update_skill/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    form = SkillForm()
    if form.validate_on_submit():
        skill.title = form.title.data
        skill.percent = form.percent.data
        db.session.commit()
        flash('Your percent has been updated!', 'success')
        return redirect(url_for('skill'))  # Redirect to the skill list page
    elif request.method == 'GET':
        form.title.data = skill.title
        form.percent.data = skill.percent
    return render_template('admin/Skills/update_skill.html', form=form, skill=skill)

@app.route('/delete/<int:skill_id>')
def delete_skill(skill_id):
    user_id = current_user.id
    skill_to_delete = Skill.query.filter_by(id=skill_id, user_id=user_id).first()

    if skill_to_delete:
        db.session.delete(skill_to_delete)
        db.session.commit()

    return redirect(url_for('skill'))