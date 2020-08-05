from flask import render_template
from app import app

@app.route('/')
def index():
    user = {'username':'Mark'}
    return render_template('index.html', title='Home',
    user=user)