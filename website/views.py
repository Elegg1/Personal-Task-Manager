import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Task, Subtask, Item
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task_name = request.form.get('task')
        if len(task_name) == 0:
            flash('New task name cannot be empty', category='error')
        else:
            return redirect(url_for('views.create_task', task_name=task_name))
    return render_template('home.html', user=current_user)

@views.route('/create-task/<task_name>', methods=['GET', 'POST'])
def create_task(task_name):
    if request.method == 'POST':
        task = Task(name=task_name, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        last_subtask_id = -1
        for di in request.form:
            if di.startswith('subtask'):
                subtask = Subtask(name=request.form.get(di), task_id=task.id)
                last_subtask_id = subtask.id
                db.session.add(subtask)
                db.session.commit()
                last_subtask_id = subtask.id

            else:
                print(last_subtask_id)
                item = Item(text=request.form.get(di), done=True, subtask_id=last_subtask_id)
                db.session.add(item)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('create_task.html', task_name=task_name, user=current_user)

@views.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = json.loads(request.data)['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})