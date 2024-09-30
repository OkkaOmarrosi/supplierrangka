from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db, login_manager
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard_bp.dashboard'))  # Redirect ke dashboard setelah login
        else:
            flash('Login gagal. Periksa username dan password.')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Contoh route yang dilindungi
@auth_bp.route('/protected')
@login_required
def protected():
    return "Ini adalah halaman yang dilindungi!"

# Ganti dashboard route di sini dengan login_required
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # Pastikan Anda memiliki dashboard.html
