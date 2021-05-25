from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subtasks = db.relationship('Subtask')
    def subtasks_done(self):
        ret = 0
        for subtask in self.subtasks:
            if subtask.done():
                ret += 1
        return ret, len(self.subtasks)

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    items = db.relationship('Item')
    def done(self):
        ret = True
        for item in self.items:
            ret = ret and item.done
        return ret
    def in_progress(self):
        ret = False
        for item in self.items:
            ret = ret or item.done
        return ret

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    subtask_id = db.Column(db.Integer, db.ForeignKey('subtask.id'))

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    second_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(50))
    tasks = db.relationship('Task')
