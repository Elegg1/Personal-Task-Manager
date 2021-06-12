import json
from flask_babel import gettext
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
            flash(gettext('New Task name cannot be empty'), category='error')
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
        err = False
        for di in request.form:
            if di.startswith('subtask'):
                if request.form.get(di) == '':
                    flash(gettext('Subtask name cannot be empty'), category='error')
                    err = True
                    subtask_name = gettext('Subtask')
                else:
                    subtask_name = request.form.get(di)
                subtask = Subtask(name=subtask_name, task_id=task.id)
                last_subtask_id = subtask.id
                db.session.add(subtask)
                db.session.commit()
                last_subtask_id = subtask.id
            else:
                if request.form.get(di) == '':
                    flash(gettext('Item text cannnot be empty'), category='error')
                    err = True
                    item_text = gettext('Item')
                else:
                    item_text = request.form.get(di)
                item = Item(text=item_text, done=False, subtask_id=last_subtask_id)
                db.session.add(item)
        db.session.commit()
        if err:
            return redirect(url_for('views.modify_task', task_id=task.id))
        return redirect(url_for('views.home'))
    task = Task(name=task_name, user_id = current_user.id)
    return render_template('modify_task.html', task=task, user=current_user, creating=True)

@views.route('/modify-task/<task_id>', methods=['GET', 'POST'])
@login_required
def modify_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return render_template('error_404.html', user=current_user, error=gettext('There is no task with that id') + f'({task_id})'), 404
    elif task.user_id != current_user.id:
        return render_template('error_403.html', user=current_user, error=gettext('You trying to access task that is not yours')), 403
    
    if request.method == 'POST':
        task = Task.query.get(task_id)
        subtask_ids, item_ids = [], []
        err = False
        for di in request.form:
            if di == 'task_name':
                if request.form.get(di) == '':
                    flash(gettext('Task name cannot be empty'), category='error')
                    err = True
                else:
                    db.session.query(Task).filter(Task.id == task.id).update({Task.name: request.form.get(di)})
                    db.session.commit()
            elif di.startswith('subtask'):
                if request.form.get(di) == '':
                    flash(gettext('Subtask name cannot be empty'), category='error')
                    err = True
                    subtask_name = gettext('Subtask')
                else:
                    subtask_name = request.form.get(di)
                if di.find('id') != -1:
                    subtask_id = int(di.split('_')[-1])
                    db.session.query(Subtask).filter(Subtask.id == subtask_id).update({Subtask.name: subtask_name})
                    db.session.commit()
                    last_subtask_id = subtask_id
                else:
                    subtask = Subtask(name=subtask_name, task_id=task.id)
                    db.session.add(subtask)
                    db.session.commit()
                    last_subtask_id = subtask.id
                subtask_ids.append(last_subtask_id)

            else:
                if request.form.get(di) == '':
                    flash(gettext('Item text cannnot be empty'), category='error')
                    err = True
                    item_text = gettext('Item')
                else:
                    item_text = request.form.get(di)
                if di.find('id') != -1:
                    item_id = int(di.split('_')[-1])
                    db.session.query(Item).filter(Item.id == item_id).update({Item.text: item_text})
                    db.session.commit()
                    item_ids.append(item_id)
                else:
                    item = Item(text=item_text, done=False, subtask_id=last_subtask_id)
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
        if err:
            return redirect(url_for('views.modify_task', task_id=task_id))
        return redirect(url_for('views.view_task', task_id=task_id))

    task = Task.query.get(task_id)
    return render_template('modify_task.html', task=task, user=current_user, creating=False)

@views.route('/task/<task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get(task_id)

    if task:
        if task.user_id != current_user.id:
            return render_template('error_403.html', user=current_user, error=gettext('You trying to access task that is not yours')), 403
        return render_template('task.html', user=current_user, task=task)
    else:
        return render_template('error_404.html', user=current_user, error=gettext('There is no task with that id') + f'({task_id})'), 404

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
    return jsonify({})