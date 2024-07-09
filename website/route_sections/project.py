# website/project.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Project, db
from website.forms import ProjectForm
from website import app
from website.routes import save_picture

project_bp = Blueprint('project', __name__)

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
                image=picture_file,
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
        flash('project added successfully', 'success')
        return redirect(url_for('project'))  # Make sure you have this route
    return render_template('admin/Projects/add_project.html', form=form)

@app.route('/dashboard/update_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            project.image = picture_file
        project.title = form.title.data
        project.description = form.description.data
        project.link = form.link.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('project'))  # Redirect to the project list page
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.link.data = project.link
    return render_template('admin/Projects/update_project.html', form=form, project=project)

@app.route('/delete/<int:project_id>')
def delete_project(project_id):
    user_id = current_user.id
    project_to_delete = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if project_to_delete:
        db.session.delete(project_to_delete)
        db.session.commit()

    return redirect(url_for('project'))