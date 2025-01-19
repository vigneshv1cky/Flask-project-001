from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"


# Initialize database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE,
            is_complete BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


init_db()


# Home route - display all tasks
@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


# Add a new task
@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        try:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                (title, description, due_date),
            )
            conn.commit()
            conn.close()
            flash("Task added successfully!", "success")
        except Exception as e:
            flash("Error adding task: " + str(e), "danger")
        return redirect(url_for("index"))
    return render_template("add_task.html")


# Edit an existing task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        cursor.execute(
            "UPDATE tasks SET title=?, description=?, due_date=? WHERE id=?",
            (title, description, due_date, task_id),
        )
        conn.commit()
        conn.close()
        flash("Task updated successfully!", "success")
        return redirect(url_for("index"))
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return render_template("edit_task.html", task=task)


# Delete a task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("index"))


# Mark a task as complete
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_complete=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    flash("Task marked as complete!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
