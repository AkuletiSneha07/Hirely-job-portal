
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import date



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    
    
    jobs = db.relationship('Job', backref='poster', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    responsibilities=db.Column(db.Text,nullable=False)
    required_skills=db.Column(db.Text,nullable=False)
    key_skills=db.Column(db.Text,nullable=False)
    company_name = db.Column(db.String(200))
    location = db.Column(db.String(100))
    experience = db.Column(db.String(255))
    salary = db.Column(db.String(50))
    image_url = db.Column(db.String(300))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('Application', backref='job', lazy=True)
    posted_date = db.Column(db.Date, default=date.today)





class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    application_date = db.Column(db.Date, default=datetime.date.today)
    status = db.Column(db.String(20), default='pending')




class MyApplication(db.Model):
    
    
    

    id = db.Column(db.Integer, primary_key=True)
    
    
    # Foreign keys and relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    job_company_name=db.Column(db.String(255))
    
    # Job application details
    job_title = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(120))
    mobile_number = db.Column(db.String(20))
    
    highest_qualification = db.Column(db.String(255))
    college_name = db.Column(db.String(255))
    specialization = db.Column(db.String(255))
    education_from_year = db.Column(db.String(4))
    education_to_year = db.Column(db.String(4))
    education_country = db.Column(db.String(255))
    
    current_job_role = db.Column(db.String(255))
    current_salary = db.Column(db.Float)
    expected_salary = db.Column(db.Float)
    
    permanent_address = db.Column(db.Text)
    
    preferred_location1 = db.Column(db.String(255))
    preferred_location2 = db.Column(db.String(255))
    key_skills = db.Column(db.Text)
    
    resume_filename = db.Column(db.String(255))

    status = db.Column(db.String(50), default='Pending')