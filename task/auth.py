import re
from flask import render_template, Blueprint, flash, redirect, url_for
from flask import request
from .models import User
from . import db
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auths = Blueprint('auths', __name__)

@auths.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            pwd_check = check_password_hash(user.password, password)
            if pwd_check:
                login_user(user)
                return redirect(url_for('view.home'))
            else:
                flash('Wrong password', category='error')
        else:
            flash('User not found')

    return render_template('login.html')

@auths.route('/signup', methods=['GET', 'POST'])
def signup():
    email_regex = re.compile('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confpass = request.form.get('confirm-password')

    if request.method == 'POST':
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('User already exists', category='error')
        elif password != confpass:
            flash('Please confirm your password', category='error')
        elif not re.fullmatch(email_regex, email):
            flash('Enter a valid email address', category='error')
        elif len(name) <  4:
            flash('Name is too short', category='error')
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auths.login'))
    return render_template('signup.html')

@auths.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auths.login'))
