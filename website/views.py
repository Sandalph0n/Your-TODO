from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
from datetime import datetime, timedelta



views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    tasks = Task.query.filter_by(userID = current_user.id).order_by(Task.deadline).all()
    name = current_user.fullname
    return render_template("home.html", tasks = tasks, name = name)


@views.route("/delete-task/<int:id>", methods=["GET"])
@login_required
def delete_task(id:int):
    current_task = Task.query.get(int(id))
    
    if current_task:
        if current_task.userID == current_user.id:
            db.session.delete(current_task)
            db.session.commit()
            flash("Delete task successfully!",category="success")
            return redirect(url_for("views.home"))
        else:
            flash("Task not found or you don't have permission to delete it!",category="error")
    else:
        flash("Task not found or you don't have permission to delete it!",category="error")

    return redirect(url_for("views.home"))

@views.route("/delete-task-noano/<int:id>", methods=["GET"])
@login_required
def delete_task_noano(id:int):
    current_task = Task.query.get(int(id))
    
    if current_task:
        if current_task.userID == current_user.id:
            db.session.delete(current_task)
            db.session.commit()
            
            return redirect(url_for("views.home"))
        else:
            pass
    else:
        pass

    return redirect(url_for("views.home"))




@views.route("/add-task", methods=["POST", "GET"])
@login_required
def add_task():
    if request.method == "GET":
        return render_template("add-task.html")
    elif request.method == "POST":
        task = dict(json.loads(request.data))
        try:
            
            taskName = task["taskName"]
            deadline = datetime.strptime(str(task["deadline"]),  "%d/%m/%Y, %H:%M:%S")
            content = task["content"]

            
            new_task = Task(name =taskName, deadline = deadline, content = content, userID = current_user.id)
            db.session.add(new_task)
            db.session.commit()
            print("Task created successfully")
            flash("Task created successfully", category="success")
            return redirect(url_for("views.home"))
        except Exception as e:
            print(e)
            flash(str(e), category="error")
            return render_template("add-task.html")



@views.route("/edit-task/<int:id>", methods=["POST","GET"])
@login_required
def edit_task(id:int):
    current_task = Task.query.get(int(id))
    taskName = current_task.name
    deadline = datetime.strftime(current_task.deadline, format="%d/%m/%Y, %H:%M:%S")
    content = current_task.content
    taskID = current_task.id

    if request.method == "POST":
        if current_task:
            if current_task.userID == current_user.id:
                pass 
            else:
                flash("Task not found or you don't have permission to edit it!",category="error")
        else:
            flash("Task not found or you don't have permission to edit it!",category="error")
    
    return render_template("edit-task.html", taskName = taskName, deadline = deadline, content= content, taskID = taskID)