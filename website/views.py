import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Task, Subtask, Item
from . import db
import random

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
@login_required
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
                item = Item(text=request.form.get(di), done=False, subtask_id=last_subtask_id)
                db.session.add(item)
        db.session.commit()
        return redirect(url_for('views.home'))
    task = Task(name=task_name, user_id = current_user.id)
    return render_template('modify_task.html', task=task, user=current_user, creating=True)

@views.route('/modify-task/<task_id>', methods=['GET', 'POST'])
@login_required
def modify_task(task_id):
    if request.method == 'POST':
        task = Task.query.get(task_id)
        subtask_ids, item_ids = [], []
        for di in request.form:
            if di.startswith('subtask'):
                if di.find('id') != -1:
                    subtask_id = int(di.split('_')[-1])
                    db.session.query(Subtask).filter(Subtask.id == subtask_id).update({Subtask.name: request.form.get(di)})
                    db.session.commit()
                    last_subtask_id = subtask_id
                else:
                    subtask = Subtask(name=request.form.get(di), task_id=task.id)
                    db.session.add(subtask)
                    db.session.commit()
                    last_subtask_id = subtask.id
                subtask_ids.append(last_subtask_id)

            else:
                if di.find('id') != -1:
                    item_id = int(di.split('_')[-1])
                    db.session.query(Item).filter(Item.id == item_id).update({Item.text: request.form.get(di)})
                    db.session.commit()
                    item_ids.append(item_id)
                else:
                    item = Item(text=request.form.get(di), done=False, subtask_id=last_subtask_id)
                    db.session.add(item)
                    db.session.commit()
                    item_ids.append(item.id)
        for subtask in task.subtasks:
            if subtask.id not in subtask_ids:
                for item in subtask.items:
                    db.session.delete(item)
                    db.session.commit()
                db.session.delete(subtask)
                db.session.commit()
            else:
                for item in subtask.items:
                    if item.id not in item_ids:
                        db.session.delete(item)
                        db.session.commit()
        db.session.commit()
        return redirect(url_for('views.view_task', task_id=task_id))

    task = Task.query.get(task_id)
    return render_template('modify_task.html', task=task, user=current_user, creating=False)

@views.route('/task/<task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get(task_id)

    if task:
        if task.user_id != current_user.id:
            return render_template('error_403.html', user=current_user, error="You trying to access task that is not yours"), 403
        return render_template('task.html', user=current_user, task=task)
    else:
        return render_template('error_404.html', user=current_user, error=f'There is no task with that id({task_id})'), 404

@views.route('/delete-task', methods=['POST'])
@login_required
def delete_task():
    task_id = json.loads(request.data)['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})

@views.route('/toggle-item', methods=['POST'])
@login_required
def toggle_item():
    item_id = json.loads(request.data)['itemId']
    item = Item.query.get(item_id)
    subtask = Subtask.query.get(item.subtask_id)
    if item:
        if Task.query.get(subtask.task_id).user_id == current_user.id:
            db.session.query(Item).filter(Item.id == item_id).update({Item.done: not item.done})
            db.session.commit()
    return jsonify({'item_done': item.done, 'subtask_done':subtask.done(), 'subtask_progress':subtask.in_progress()})


@views.route('/get-item-done/<item_id>')
@login_required
def get_item_done(item_id):
    print(1)
    item = Item.query.get(item_id)
    db.session.query(Item).filter(Item.id == item_id).update({Item.done: not item.done})
    db.session.commit()
    return jsonify({'done': item.done})

@views.route('/get-subtask-done/<item_id>')
@login_required
def get_subtask_done(item_id):
    item = Item.query.get(item_id)
    subtask = Subtask.query.get(item.subtask_id)
    return jsonify({'done': subtask.done(), 'progress': subtask.in_progress()})