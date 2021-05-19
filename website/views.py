import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('note')
        if len(text) == 0:
            flash('Note cannot be empty', category='error')
        else:
            new_note = Note(text=text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note_id = json.loads(request.data)['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})