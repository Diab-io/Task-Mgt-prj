from flask import Flask, render_template, Blueprint

auths = Blueprint('auths', __name__)

@auths.route('/login')
def login():
    return render_template('login.html')

@auths.route('/signup')
def signup():
    return render_template('signup.html')
