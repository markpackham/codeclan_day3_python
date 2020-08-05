from flask import render_template
from app import app

# the "u" in the title area is for handling Unicode
@app.route('/')
def index():
    user = {'username':'Mark'}
    tasks = [
        {
            'id': 1,
            'title': u'Buy groceries',
            'description': 'Milk, Cheese, Pizza, Fruit',
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': 'Learn an awesome new programming language',
            'done': True
        }
    ]
    return render_template('index.html', title='Home',
    user=user, tasks = tasks)