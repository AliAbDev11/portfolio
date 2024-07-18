# website/project.py
import os
import secrets
from PIL import Image
from flask import Blueprint, current_app, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Project, db
from website.forms import ProjectForm
from website import app

project_bp = Blueprint('project', __name__)

# Helper function to save uploaded pictures
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/images", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route('/dashboard/list_projects', methods=['GET'])
@login_required
def project():
    user_id = current_user.id
    title = request.args.get('title', '')

    query = Project.query.filter_by(user_id=user_id)

    if title:
        query = query.filter(Project.title.ilike(f'%{title}%'))

    projects = query.all()

    return render_template('admin/Projects/list_projects.html', projects=projects)

@app.route('/dashboard/add_project', methods=["GET", "POST"])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            project = Project(
                title=form.title.data,
                description=form.description.data,
                link=form.link.data,
                picture=picture_file,
                user_id=current_user.id
            )
        else:
            project = Project(
                title=form.title.data,
                description=form.description.data,
                link=form.link.data,
                user_id=current_user.id
            )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully', 'success')
        return redirect(url_for('project'))
    return render_template('admin/Projects/add_project.html', form=form)

@app.route('/dashboard/update_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.link = form.link.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            project.picture = picture_file
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('project'))
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.link.data = project.link
    return render_template('admin/Projects/update_project.html', form=form, project=project)

@app.route('/dashboard/delete_project/<int:project_id>')
@login_required
def delete_project(project_id):
    user_id = current_user.id
    project_to_delete = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if project_to_delete:
        db.session.delete(project_to_delete)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    else:
        flash('Project not found or you do not have permission to delete this project.', 'danger')

    return redirect(url_for('project'))