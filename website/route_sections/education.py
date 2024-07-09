# website/education.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from website.models import Education, db
from website.forms import EducationForm
from website import app

education_bp = Blueprint('education', __name__)

@app.route('/dashboard/list_educations', methods=['GET'])
@login_required
def education():
    user_id = current_user.id
    degree = request.args.get('degree', '')
    school = request.args.get('school', '')

    query = Education.query.filter_by(user_id=user_id)

    if degree:
        query = query.filter(Education.degree.ilike(f'%{degree}%'))
    if school:
        query = query.filter(Education.school.ilike(f'%{school}%'))

    educations = query.all()

    return render_template('admin/Educations/list_educations.html', educations=educations)

@app.route('/dashboard/add_education', methods=["GET", "POST"])
@login_required
def add_education():
    form = EducationForm()
    if form.validate_on_submit():
        end_date = None if form.is_current.data else form.end_date.data
        new_education = Education(
            degree=form.degree.data,
            school=form.school.data,
            start_date=form.start_date.data,
            end_date=end_date,
            is_current=form.is_current.data,
            address=form.address.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_education)
        db.session.commit()
        flash('Education added successfully', 'success')
        return redirect(url_for('education'))
    return render_template('admin/Educations/add_education.html', form=form)

@app.route('/dashboard/update_education/<int:education_id>', methods=['GET', 'POST'])
@login_required
def update_education(education_id):
    education = Education.query.get_or_404(education_id)
    form = EducationForm()
    if form.validate_on_submit():
        education.degree = form.degree.data
        education.school = form.school.data
        education.start_date = form.start_date.data
        education.end_date = form.end_date.data if not form.is_current.data else None
        education.is_current = form.is_current.data
        education.address = form.address.data
        education.description = form.description.data
        db.session.commit()
        flash('Your education has been updated!', 'success')
        return redirect(url_for('education'))  # Redirect to the education list page
    elif request.method == 'GET':
        form.degree.data = education.degree
        form.school.data = education.school
        form.start_date.data = education.start_date
        form.end_date.data = education.end_date
        form.is_current.data = education.is_current
        form.address.data = education.address
        form.description.data = education.description
    return render_template('admin/Educations/update_education.html', form=form, education=education)

@app.route('/delete/<int:education_id>')
def delete_education(education_id):
    user_id = current_user.id
    education_to_delete = Education.query.filter_by(id=education_id, user_id=user_id).first()

    if education_to_delete:
        db.session.delete(education_to_delete)
        db.session.commit()

    return redirect(url_for('education'))