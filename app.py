
# from flask import Flask
# from routes import auth, jobs, admin
# import os
# from dotenv import load_dotenv
# from extensions import db, login_manager

# load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # CHANGE: Replace with your MySQL connection string
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # CHANGE: Replace with a strong secret key
# db.init_app(app)
# login_manager.init_app(app)
# login_manager.login_view = 'auth.login'

# app.register_blueprint(auth.auth_bp)
# app.register_blueprint(jobs.jobs_bp)
# app.register_blueprint(admin.admin_bp)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

from routes import auth, jobs, admin
import os
from dotenv import load_dotenv
from extensions import db, login_manager
from flask_login import login_required, current_user
from routes import jobs

# from flask_mysqldb import MySQL
import re
from models import User

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.unauthorized_handler
def unauthorized():
    flash("Login Required..!", "warning")
    return redirect(url_for("auth.login"))

app.register_blueprint(auth.auth_bp)
app.register_blueprint(jobs.jobs_bp)
app.register_blueprint(admin.admin_bp)

@app.route("/check_email")
def check_email():
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()
    return jsonify({"exists": bool(user)})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

       
        if not re.match(r"^(?=.*[A-Z])(?=.*[\W_]).{8,}$", password):
            flash("Password must be 8+ characters, 1 uppercase & 1 special character.", "danger")
            return redirect(url_for("register"))

        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

       
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        
        new_user = User(username=username, email=email)
        new_user.set_password(password)  
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/employe')
def employe():
    return render_template('employe.html')






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
