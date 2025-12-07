from flask import render_template, request, redirect, url_for, Blueprint, flash
from models import Job, Application, MyApplication
from extensions import db
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from sqlalchemy import and_


jobs_bp = Blueprint('jobs', __name__)

UPLOAD_FOLDER = 'uploads' 
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@jobs_bp.route('/')
@login_required
def index():
    return redirect(url_for('jobs.jobs'))

@jobs_bp.route('/jobs')
@login_required
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@jobs_bp.route('/adminjobs')
@login_required
def adminjobs():
    jobs = Job.query.all()
    return render_template('admin_job.html', jobs=jobs)


@jobs_bp.route('/employejobs')
@login_required
def employejobs():
    jobs = Job.query.all()
    return render_template('employe_job.html', jobs=jobs)


@jobs_bp.route('/job/<int:job_id>')
@login_required
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@jobs_bp.route('/admin/job/<int:job_id>')
@login_required
def admin_job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('admin_job_details.html', job=job)

@jobs_bp.route('/employe/job/<int:job_id>')
@login_required
def employe_job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('employe_job_details.html', job=job)




@jobs_bp.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        return "Access denied"
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company_name = request.form['company_name']
        location = request.form['location']
        salary = request.form['salary']
       
        job = Job(title=title, description=description, company_name=company_name, location=location, salary=salary)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs.jobs'))
    return render_template('post_job.html')
@jobs_bp.route('/search', methods=['GET'])
@login_required
def search():
    title = request.args.get('title')  
    location = request.args.get('location')  

   
    query = Job.query

    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    jobs = query.all()

   
    if not jobs:
        return render_template('jobs.html', message="No matches found.")

    return render_template('jobs.html', jobs=jobs)
@jobs_bp.route('/apply/<int:job_id>')
@login_required
def apply(job_id):
    application = Application(user_id=current_user.id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('jobs.jobs'))

@jobs_bp.route('/search', methods=['GET'])
@login_required
def search_jobs():
    location = request.args.get('location')
    title = request.args.get('title')
    query = Job.query
    jobs = []

    if location and title:
        jobs = query.filter(Job.location.ilike(f"%{location}%"), Job.title.ilike(f"%{title}%")).all()
    elif location:
        jobs = query.filter(Job.location.ilike(f"%{location}%")).all()
    elif title:
        jobs = query.filter(Job.title.ilike(f"%{title}%")).all()
    else:
        jobs = query.all()

    if not jobs and (location or title): 
        message = "No results found."
        return render_template('search_jobs.html', jobs=jobs, message=message)
    else:
        return render_template('search_jobs.html', jobs=jobs, message=None)

@jobs_bp.route('/apply_form/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_form(job_id):
    job = Job.query.get_or_404(job_id)
    job_company_name = job.company_name
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        preferred_location1 = request.form['preferred_location1']
        preferred_location2 = request.form['preferred_location2']
        key_skills = request.form['key_skills']
        file = request.files['resume']
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        highest_qualification = request.form.get('highest_qualification')
        college_name = request.form.get('college_name')
        specialization = request.form.get('specialization')
        education_from_year = request.form.get('education_from_year')
        education_to_year = request.form.get('education_to_year')
        education_country = request.form.get('education_country')
        current_job_role = request.form.get('current_job_role')
        current_salary = request.form.get('current_salary')
        expected_salary = request.form.get('expected_salary')
        permanent_address = request.form.get('permanent_address')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            application = MyApplication(
                user_id=current_user.id,
                job_id=job_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                job_title=job.title,
                job_company_name = job.company_name,
                email=email,
            mobile_number=mobile_number,
            highest_qualification=highest_qualification,
            college_name=college_name,
            specialization=specialization,
            education_from_year=education_from_year,
            education_to_year=education_to_year,
            education_country=education_country,
            current_job_role=current_job_role,
            current_salary=current_salary,
            expected_salary=expected_salary,
            permanent_address=permanent_address,
                preferred_location1=preferred_location1,
                preferred_location2=preferred_location2,
                key_skills=key_skills,
                resume_filename=filename
            )
            db.session.add(application)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('jobs.my_applications'))
        else:
            flash('Invalid file or no file uploaded.', 'error')
            return redirect(url_for('jobs.apply_form', job_id=job_id))

    return render_template('apply_form.html', job=job)

@jobs_bp.route('/my_applications')
@login_required
def my_applications():
    applications = MyApplication.query.filter_by(user_id=current_user.id).all()
    return render_template('my_applications.html', applications=applications)
    
@jobs_bp.route('/applications')
@login_required
def applications():
    applications = MyApplication.query.all()  
    return render_template('applications.html', applications=applications)


@jobs_bp.route('/delete_application/<int:application_id>', methods=['POST'])
@login_required
def delete_application(application_id):
    
    application = MyApplication.query.filter_by(id=application_id, user_id=current_user.id).first()

    if application:
        db.session.delete(application)
        db.session.commit()
        flash('Application deleted successfully!', 'success')
    else:
        flash('Application not found or you do not have permission to delete this.', 'error')

    return redirect(url_for('jobs.my_applications'))

@jobs_bp.route('/delete_applications/<int:application_id>', methods=['POST'])
@login_required
def delete_applications(application_id):
    application = MyApplication.query.get_or_404(application_id)

    

    application.status = 'rejected'
    db.session.commit()
    flash('Application status changed to rejected.', 'warning')
    return redirect(url_for('jobs.applications'))

@jobs_bp.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company_name = request.form.get('company_name')
        location = request.form.get('location')
        salary = request.form.get('salary')
        responsibilities = request.form.get('responsibilities')
        required_skills = request.form.get('required_skills')
        key_skills = request.form.get('key_skills')

        
        print(f"Title: {title}, Description: {description}, Company: {company_name}, Location: {location}, Salary: {salary}")

        
        if not title or not description or not company_name or not location or not salary:
            flash('All fields are required!', 'danger')
            return render_template('edit_job.html', job=job)

        
        job.title = title
        job.description = description
        job.company_name = company_name
        job.location = location
        job.salary = salary
        job.responsibilities =responsibilities
        job.required_skills = required_skills
        job.key_skills = key_skills




        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs.adminjobs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating job: {e}', 'danger')

    return render_template('edit_job.html', job=job)

@jobs_bp.route('/employe_edit_job/<int:job_id>', methods=['GET', 'POST'])
def employe_edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company_name = request.form.get('company_name')
        location = request.form.get('location')
        salary = request.form.get('salary')
        responsibilities = request.form.get('responsibilities')
        required_skills = request.form.get('required_skills')
        key_skills = request.form.get('key_skills')

        
        print(f"Title: {title}, Description: {description}, Company: {company_name}, Location: {location}, Salary: {salary}")

        
        if not title or not description or not company_name or not location or not salary:
            flash('All fields are required!', 'danger')
            return render_template('employe_edit_job.html', job=job)

        
        job.title = title
        job.description = description
        job.company_name = company_name
        job.location = location
        job.salary = salary
        job.responsibilities =responsibilities
        job.required_skills = required_skills
        job.key_skills = key_skills




        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs.employejobs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating job: {e}', 'danger')

    return render_template('employe_edit_job.html', job=job)

@jobs_bp.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()
    flash('Job posting deleted successfully!', 'success')
    return redirect(url_for('jobs.adminjobs'))

@jobs_bp.route('/employe_delete_job/<int:job_id>', methods=['POST'])
@login_required
def employe_delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()
    flash('Job posting deleted successfully!', 'success')
    return redirect(url_for('jobs.employejobs'))

@jobs_bp.route('/post_jobs', methods=['GET', 'POST'])
@login_required
def post_jobs():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        responsibilities = request.form.get('responsibilities')
        required_skills = request.form.get('required_skills')
        key_skills = request.form.get('key_skills')
        company_name = request.form.get('company_name')
        location = request.form.get('location')
        experience = request.form.get('experience')
        salary = request.form.get('salary')
        image_url = request.form.get('image_url')  

       
        if not all([title, description, responsibilities, required_skills, key_skills, company_name, location, experience, salary]):
            flash('All fields are required.', 'danger')
            return render_template('post_jobs.html')

        job = Job(
            title=title,
            description=description,
            responsibilities=responsibilities,
            required_skills=required_skills,
            key_skills=key_skills,
            company_name=company_name,
            location=location,
            experience=experience,
            salary=salary,
            image_url=image_url,
            user_id=current_user.id
        )

        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('jobs.employejobs'))

    return render_template('post_jobs.html')


@jobs_bp.route('/shortlist/<int:application_id>', methods=['POST'])
@login_required
def shortlist_applications(application_id):
    application = MyApplication.query.get_or_404(application_id)
    application.status = 'shortlisted'
    db.session.commit()
    flash('Application shortlisted successfully!', 'success')
    return redirect(url_for('jobs.applications'))  