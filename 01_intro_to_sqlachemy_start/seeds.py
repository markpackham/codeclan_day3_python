from app import db
from app.models import User, Task

Task.query.delete()
User.query.delete()

user = User(username='Mark')
db.session.add(user)
db.session.commit()

users = User.query.all()
print(users)

user = users[0]
print(user.id, user.username)

user = User.query.get(1)
task1 = Task(title='Learn Python', description="Learn how to code in Python", done=True, user=user)
db.session.add(task1)
task2 = Task(title='Buy Milk', description="I need milk for my tea!", user=user)
db.session.add(task2)
db.session.commit()

tasks = Task.query.all()
print(tasks)

task_user = Task.query.get(1).user
print(user.username)