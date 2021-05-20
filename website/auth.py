from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password', category='error')
        else:
            flash('Wrong email', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        first_name = data.get('firstName')
        password = data.get('password')
        pwd_confirm = data.get('passwordConfirm')
        error = False
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account with this email already exists', category='error')
            return render_template('sign_up.html')
        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
            error = True
        if len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
            error = True
        if password != pwd_confirm:
            flash('Password and password confirm must be equal', category='error')
            error = True
        if not error:
            new_user = User(email=email, name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)