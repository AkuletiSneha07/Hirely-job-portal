from flask import render_template, redirect, url_for, Blueprint
from models import User, Job, MyApplication
from extensions import db
from flask_login import login_required, current_user
from flask import request, flash


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        return "Access denied"
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/jobs')
@login_required
def admin_jobs():
    if current_user.role != 'admin':
        return "Access denied"
    jobs = Job.query.all()
    return render_template('admin/jobs.html', jobs=jobs) 

@admin_bp.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return "Access denied"
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/delete_job/<int:job_id>')
@login_required
def delete_job(job_id):
    if current_user.role != 'admin':
        return "Access denied"
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('admin.admin_jobs'))

# @admin_bp.route('/admin/applications')
# @login_required
# def admin_applications():
#     if current_user.role != 'admin':
#         return "Access denied"
    
#     applications = MyApplication.query.all()
#     return render_template('admin/applications.html', applications=applications)

# @admin_bp.route('/admin/applications/<int:application_id>/shortlist', methods=['POST'])
# @login_required
# def shortlist_application(application_id):
#     if current_user.role != 'admin':
#         return "Access denied"
    
#     application = MyApplication.query.get_or_404(application_id)
#     application.status = "shortlisted"
#     db.session.commit()
#     flash("Application shortlisted successfully", "success")
#     return redirect(url_for('admin.admin_applications'))


# @admin_bp.route('/admin/applications/<int:application_id>/reject', methods=['POST'])
# @login_required
# def reject_application(application_id):
#     if current_user.role != 'admin':
#         return "Access denied"
    
#     application = MyApplication.query.get_or_404(application_id)
#     application.status = "rejected"
#     db.session.commit()
#     flash("Application rejected successfully", "danger")
#     return redirect(url_for('admin.admin_applications'))

@admin_bp.route('/admin/users_by_email')
@login_required
def admin_users_by_email():
    if current_user.email != "admin@example.com":
        return "Access denied"
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/applications')
def admin_applications():
    applications = MyApplication.query.all()
    return render_template('applications.html', applications=applications)

@admin_bp.route('/admin/applications/<int:application_id>/shortlist', methods=['POST'])
def shortlist_application(application_id):
    application = MyApplication.query.get_or_404(application_id)
    application.status = "shortlisted"
    db.session.commit()
    flash("Application shortlisted successfully", "success")
    return redirect(url_for('admin.applications'))

@admin_bp.route('/admin/applications/<int:application_id>/reject', methods=['POST'])
def reject_application(application_id):
    application = MyApplication.query.get_or_404(application_id)
    application.status = "rejected"
    db.session.commit()
    flash("Application rejected successfully", "danger")
    return redirect(url_for('admin.applications'))

