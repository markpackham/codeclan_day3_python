from app import db
from app.models import User, Task
Task.query.delete()
User.query.delete()
user1 = User(username="Eugene")
user2 = User(username="Zsolt")
db.session.add(user1)
db.session.add(user2)
db.session.commit()
users = User.query.all()
print(users)