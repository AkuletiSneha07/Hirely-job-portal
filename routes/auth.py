
from flask import render_template, request, redirect, url_for, Blueprint, session
from models import User
from extensions import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask import flash


auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            print("User added successfully")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Error adding user: {e}")
            return "Already Registered...."

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            session['user_id'] = user.id

            
            if username == "admin":
                return redirect(url_for('admin'))  
            elif username == "employe":
                return redirect(url_for('employe')) 
            else:
                return redirect(url_for('jobs.jobs'))  

        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html', error=None)

@auth_bp.route('/users')
@login_required
def users():
    all_users = User.query.all()  
    return render_template('display_users.html', users=all_users)

@auth_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('auth.users'))
    
    return render_template('edit_user.html', user=user)

@auth_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('auth.users'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))