import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('task')
        if len(text) == 0:
            flash('Task name cannot be empty', category='error')
        else:
            new_task = Task(name=text, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added', category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = json.loads(request.data)['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})