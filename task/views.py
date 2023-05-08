from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Todo
from . import db

view = Blueprint('view', __name__)

@view.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task = request.form.get('created_task')
        if task:
            todo = Todo(text=task, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
        else:
            flash('Please add a todo text')
    user_todos = Todo.query.filter_by(user_id=current_user.id)
    return render_template('home.html', user=current_user.name, todos=user_todos)

@view.route('/post-delete/<id>')
@login_required
def delete_post(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('view.home'))
