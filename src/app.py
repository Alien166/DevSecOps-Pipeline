from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.route("/", methods=["GET"])
def home():
    return redirect("/tasks")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    tasks = load_tasks()
    if request.method == "POST":
        new_task = request.form.get("task")
        if new_task:
            tasks.append({"text": new_task, "done": False})
            save_tasks(tasks)
        return redirect("/tasks")
    return render_template("tasks.html", tasks=tasks)

@app.route("/tasks/toggle/<int:index>")
def toggle_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
    return redirect("/tasks")

@app.route("/tasks/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect("/tasks")

@app.route("/scan-logs")
def scan_logs():
    try:
        with open("scan.log") as f:
            logs = f.read()
    except FileNotFoundError:
        logs = "No scan log available."
    return render_template("scan_logs.html", logs=logs)

@app.route("/summary")
def summary():
    try:
        with open("pipeline_status.json") as f:
            status = json.load(f)
    except FileNotFoundError:
        status = {
            "last_build": "N/A",
            "status": "unknown",
            "last_deploy": "N/A"
        }
    return render_template("summary.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
