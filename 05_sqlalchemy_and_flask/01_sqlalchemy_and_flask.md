# Flask and SqlAlchemy

**Duration: 60 minutes**

## Learning Objectives

- Use SqlAlchemy to implement RESTful routes.

## Introduction

So now that we have SqlAlchemy set up and have our seed data let's use that to pass the data to our templates from the routes file.

We will use the RESTful routes to implement our database CRUD actions.

There are 7 routes in order to give a browser user access to our CRUD actions. In fact, these 7 routes make up a pretty handy design pattern or convention for designing apps which access a database through a browser, called REST.

REST stands for RE-presentational S-tate T-ransfer, but no one really cares. You are much more likely to run into the phrase 'RESTful APIs'. An API is just the way in which one application expects to be talked to by another application; in this case, it's how a database application talks to a web browser. And by following the RESTful convention, we make our application more useable. The convention is so widespread that the actions we can perform are predictable. Developers like when things are predictable!

|VERB  |PATH                    |ACTION |
|:----:|:----------------------:|:-----:|
|GET   |/tasks                  |index  |
|GET   |/tasks/:id              |show   |
|GET   |/tasks/new              |new    |
|POST  |/tasks                  |create |
|GET   |/tasks/:id/edit         |edit   |
|POST  |/tasks/:id              |update |
|POST  |/tasks/:id/delete       |destroy|

### Index Route

We can start by changing the index route to get the user and all their tasks from the database instead of using our 'Dummy' data.

At the top of the file we will import `db` and our models.

```python
# route.py
from app import app, db # MODIFIED
from app.models import User, Task # ADDED
```

Next we can remove the hard coded data from the index route. While we are doing this let's change the route to `/tasks` to make it more RESTful.

```python
# routes.py
@app.route('/tasks')
def index(): # MODIFIED
    return render_template('index.html', title='Home', user=user, tasks=tasks)
```

So we still want to pass the user and tasks through to the index template.

We will start by getting the user from the database. (For now we will still just be using the one user so will use their id in the database. Normally this may have been passed through from a login page.)

```python
# routes.py
@app.route('/tasks')
def index():
    user = User.query.get(1)
    return render_template('index.html', title='Home', user=user, tasks=tasks)
```

And next we can get the tasks. As we only want to see tasks relating to the "logged in" user, and we also have the relationship set up between the two models, we can use the tasks file of this user instance instead of querying the database again.

```python
# routes.py
@app.route('/tasks')
def index():
    user = User.query.get(1)
    tasks = user.tasks
    return render_template('index.html', title='Home', user=user, tasks=tasks)
```

OK now if we go to our browser (starting the server if not already running) we should see the details from our database coming through.


### Adding a task

Next step is to add a task.

We will create a form and set the action to make a POST request to a `/tasks` route.

Let's start by adding a from to the top of the index template.

```html
{% block content %}

    <form action="/tasks" method="POST">
      <label for="title">Title:</label>
      <input type="text" name="title" id="title" />
      <label for="description">Description:</label>
      <textarea name="description" id="description" rows="4" cols="80"></textarea>
      <input type="submit" value="Add Task">
    </form>
    <h1>Hi, {{ user.name }}!</h1>
    <!-- ... AS BEFORE -->
{% endblock %}
```

Note that our form fields have a `name` attribute that corresponds to the properties of the task. This will make it easier to create the task to save.

We will create a new route function in `routes.py ` for our CREATE route. Do this just below our index function.

As this needs to be a POST method we will inforn the decorator of this. We can declare which methods are used for this route. This is passed as a list. We only want `POST` for this route.

For now we will just have it return a string so that we can see what is happening later.

```python

@app.route('/tasks', methods=['POST'])
def create():
return 'Done'
```

We will need the user object to assign to the task so let's get that from our database first.

```python
#routes.py

@app.route('/tasks', methods=['POST'])
def create():
  user = User.query.get(1)
  return 'Done'
```

Next we need to access the form data to create the new task.

### Accessing form data in our application.

Go to the browser and open the inspector tools (cmd+option+i).

Our HTML tells the form what to do when the Submit button is clicked. It actually sends a new HTTP Request to the server, which we can view in the Chrome Dev Tools:

- Go to Network tab
- Fill out form and hit submit
- Select document that pops up in Network tab (404?) and look at Headers tab

The submit button is sending an HTTP POST request to `/tasks`, which is what we put in the HTML <form> method and action.

Actually this is why we used a form in the first place. An HTML form can send any HTTP request type we want, but the address bar of a browser can only send GET requests. This is a security feature. It means that users can't just POST any stuff they want to our server. We get to control the data they POST with our form inputs.

If we scroll to the bottom of that Headers tab, we can see our form data! So not only is the form making an HTTP POST request, it is sending our form data back to the server.

So we need to access that form data in the server to create a new database entry.

### Accessing the form data

To access the form in our routes.py file we will need to get access to the request that is being made.

Fortunately for us Flask makes that simple. Flask comes with a request object that we can import into our file.

```python
# routes.py

from flask import render_template, request # MODIFIED
from app import app, db
from app.models import User, Task

```

And now in our route we can access the form by calling `request.form`.

Let's print it out and see what we get.

```python
#routes.py

@app.route('/tasks', methods=['POST'])
def create():
  user = User.query.get(1)
  print(request.form)
  return 'Done'
```

IF we submit the form and look at the terminal we can see that the request.form is a type of dictionary, `ImmutableMultiDict`.

We should also see the form values as key value pairs. So we can access these using the keys and create a new task.

```python
#routes.py

@app.route('/tasks', methods=['POST'])
def create():
  user = User.query.get(1)
  taskTitle = request.form['title']
  taskDesc = request.form['description']
  newTask = Task(title=taskTitle, description=taskDesc, user=user)
  return 'Done'
```

And finally save that task to the database.

```python
#routes.py

@app.route('/tasks', methods=['POST'])
def create():
  user = User.query.get(1)
  taskTitle = request.form['title']
  taskDesc = request.form['description']
  newTask = Task(title=taskTitle, description=taskDesc, user=user)
  db.session.add(newTask)
  db.session.commit()
  return 'Done'
```

After the task has been added we probably want to redirect back to our index route to see the list of tasks with the new one.

We can import `redirect` from Flask and use that insead of returning a string.

```python
#routes.py
from flask import render_template, request, redirect # MODIFIED
from app import app, db
from app.models import User, Task

#...
@app.route('/tasks', methods=['POST'])
def create():
  user = User.query.get(1)
  taskTitle = request.form['title']
  taskDesc = request.form['description']
  newTask = Task(title=taskTitle, description=taskDesc, user=user)
  db.session.add(newTask)
  db.session.commit()
  return redirect('/tasks') # MODIFIED
```

And now when we submit our form our task should be displayed in the list.

# Editing a task

Lastly we will update a task to be completed.

As you may imagine this will require another route to be coded. The route we will hit will be `/tasks/{theTaskId}`.

Normally update requests would be sent as a `PUT` request. As we are making requests from the browser we only get access to `GET` and `POST` requests. As we will be modifying the data we will use a form and make a `POST` request.

For quickness we will also cheekily add some inline styling so that the button appears next to the text (sshh.. don't tell anyone!)

```html
<!-- index.html -->

<div>
      {{ task.title }}: <b>{{ task.description }}</b>
        {% if task.done %}
        <span> &#9989;</span>
        {% else %}
        <span>
          <form style="display:inline" action="/tasks/{{task.id}}" method="POST">
            <input type="submit" value="Mark as complete">
          </form>
        </span>
        {% endif %}
    </div>
```

So when we click the button we will make a post request to our server.

Let's write the route to handle this request. To get access to parameters in our route we can put the keyword inside a tag with the following syntax: `<type:name>`. This informs flask that this is a variable that will be part of the url and also what type it is.

We then pass that variable into the routes handler method.

```python
# route.py

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update(task_id):

    return redirect('/')
```

So in here we will first of all use the id to find the task we want to update.

```python
# route.py

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id) # ADDED
    return redirect('/')
```

And next we will set the `done` property of the task to true.

```python
# route.py

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    task.done = True # ADDED
    return redirect('/')
```

And lastly we will call `commit()` and this will save any changes to the task to the database.

```python
# route.py

@app.route('/tasks/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    task.done = True # ADDED
    db.session.commit()
    return redirect('/')
```

If we now go to the browser, refresh, and click on the button our task should update.

## Summary

We can create routes in flask using the `@app.route` decorator. We can also specify which type of requests this route will be used for. Routes can be used for multiple request types.

We can pass parameters into the route via the url. To access the parameters we use the syntax `<type:name>` to declare that this is a variable parameter. This can then be passed directly into the route handler method.
