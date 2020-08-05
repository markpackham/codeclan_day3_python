from flask import render_template, request, redirect
from app import app, db
from app.models import User, Task

@app.route('/tasks')
def index():
    user = User.query.get(1)
    tasks = user.tasks
    return render_template('index.html', title='Home', user=user, tasks=tasks)


@app.route('/tasks', methods=['POST'])
def create():
    user = User.query.get(1)
    task = Task(title = request.form['title'],
    description = request.form['description'],
    user = user)
    db.session.add(task)
    db.session.commit()
    return redirect('/tasks')

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    task.done = True
    db.session.commit()
    return redirect('/tasks')
