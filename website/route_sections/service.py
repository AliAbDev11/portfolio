# website/service.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Service, db
from website.forms import ServiceForm
from website import app
from website.routes import save_picture

service_bp = Blueprint('service', __name__)

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
                image=picture_file,
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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            service.image = picture_file
        service.title = form.title.data
        service.description = form.description.data
        db.session.commit()
        flash('Your service has been updated!', 'success')
        return redirect(url_for('service'))  # Redirect to the service list page
    elif request.method == 'GET':
        form.title.data = service.title
        form.description.data = service.description
    return render_template('admin/Services/update_service.html', form=form, service=service)

@app.route('/delete/<int:service_id>')
def delete_service(service_id):
    user_id = current_user.id
    service_to_delete = Service.query.filter_by(id=service_id, user_id=user_id).first()

    if service_to_delete:
        db.session.delete(service_to_delete)
        db.session.commit()

    return redirect(url_for('service'))