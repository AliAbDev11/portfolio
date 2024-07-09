# website/experience.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Experience, db
from website.forms import ExperienceForm
from website import app

experience_bp = Blueprint('experience', __name__)

@app.route('/dashboard/list_experiences', methods=['GET'])
@login_required
def experience():
    user_id = current_user.id
    job_title = request.args.get('job_title', '')
    company_name = request.args.get('company_name', '')

    query = Experience.query.filter_by(user_id=user_id)

    if job_title:
        query = query.filter(Experience.job_title.ilike(f'%{job_title}%'))
    if company_name:
        query = query.filter(Experience.company_name.ilike(f'%{company_name}%'))

    experiences = query.all()

    return render_template('admin/Experiences/list_experiences.html', experiences=experiences)

@app.route('/dashboard/add_experience', methods=["GET", "POST"])
@login_required
def add_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        end_date = None if form.is_current.data else form.end_date.data
        new_experience = Experience(
            job_title=form.job_title.data,
            company_name=form.company_name.data,
            start_date=form.start_date.data,
            end_date=end_date,
            is_current=form.is_current.data,
            address=form.address.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_experience)
        db.session.commit()
        flash('Experience added successfully', 'success')
        return redirect(url_for('experience'))
    return render_template('admin/Experiences/add_experience.html', form=form)

@app.route('/dashboard/update_experience/<int:experience_id>', methods=['GET', 'POST'])
@login_required
def update_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    form = ExperienceForm()
    if form.validate_on_submit():
        experience.job_title = form.job_title.data
        experience.company_name = form.company_name.data
        experience.start_date = form.start_date.data
        experience.end_date = form.end_date.data if not form.is_current.data else None
        experience.is_current = form.is_current.data
        experience.address = form.address.data
        experience.description = form.description.data
        db.session.commit()
        flash('Your experience has been updated!', 'success')
        return redirect(url_for('experience'))  # Redirect to the experience list page
    elif request.method == 'GET':
        form.job_title.data = experience.job_title
        form.company_name.data = experience.company_name
        form.start_date.data = experience.start_date
        form.end_date.data = experience.end_date
        form.is_current.data = experience.is_current
        form.address.data = experience.address
        form.description.data = experience.description
    return render_template('admin/Experiences/update_experience.html', form=form, experience=experience)

@app.route('/delete/<int:experience_id>')
def delete_experience(experience_id):
    user_id = current_user.id
    experience_to_delete = Experience.query.filter_by(id=experience_id, user_id=user_id).first()

    if experience_to_delete:
        db.session.delete(experience_to_delete)
        db.session.commit()

    return redirect(url_for('experience'))