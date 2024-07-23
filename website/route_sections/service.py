# website/service.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Service, db
from website.forms import ServiceForm
from website import app
from PIL import Image
import secrets
import os

service_bp = Blueprint('service', __name__)

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

@app.route('/dashboard/list_services', methods=['GET'])
@login_required
def service():
    user_id = current_user.id
    title = request.args.get('title', '')

    query = Service.query.filter_by(user_id=user_id)

    if title:
        query = query.filter(Service.title.ilike(f'%{title}%'))

    services = query.all()

    return render_template('admin/Services/list_services.html', services=services)

@app.route('/dashboard/add_service', methods=["GET", "POST"])
@login_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            service = Service(
                title=form.title.data,
                description=form.description.data,
                picture=picture_file,
                user_id=current_user.id
            )
        else:
            service = Service(
                title=form.title.data,
                description=form.description.data,
                user_id=current_user.id
            )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully', 'success')
        return redirect(url_for('service'))  # Make sure you have this route
    return render_template('admin/Services/add_service.html', form=form)

@app.route('/dashboard/update_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            service.picture = picture_file
        db.session.commit()
        flash('Your service has been updated!', 'success')
        return redirect(url_for('service'))  # Redirect to the service list page
    elif request.method == 'GET':
        form.title.data = service.title
        form.description.data = service.description
    return render_template('admin/Services/update_service.html', form=form, service=service)

@app.route('/delete/delete_service/<int:service_id>')
def delete_service(service_id):
    user_id = current_user.id
    service_to_delete = Service.query.filter_by(id=service_id, user_id=user_id).first()

    if service_to_delete:
        db.session.delete(service_to_delete)
        db.session.commit()
        flash('Service deleted successfully', 'success')
    else:
        flash('Service not found or you do not have permission to delete this service.', 'danger')

    return redirect(url_for('service'))