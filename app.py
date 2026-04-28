"""
To-Do Application — Flask + JSON File Storage
Full CRUD: Add, Edit, Delete, Search & Filter
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# ─── File Handling Config ─────────────────────────────────────────────────────
DATA_FILE = "tasks.json"


def load_tasks() -> list[dict]:
    """Read all tasks from the JSON file. Returns empty list if file missing."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks: list[dict]) -> None:
    """Write the full tasks list back to the JSON file (pretty-printed)."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def find_task(tasks: list[dict], task_id: str) -> dict | None:
    """Return the task dict matching task_id, or None."""
    return next((t for t in tasks if t["id"] == task_id), None)


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    query  = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "all")   # all | pending | done

    tasks = load_tasks()

    # Filter by search query
    if query:
        tasks = [t for t in tasks if query in t["title"].lower()
                                  or query in t.get("description", "").lower()]

    # Filter by status
    if status == "pending":
        tasks = [t for t in tasks if not t["done"]]
    elif status == "done":
        tasks = [t for t in tasks if t["done"]]

    return render_template("index.html",
                           tasks=tasks,
                           query=request.args.get("q", ""),
                           status=status,
                           total=len(load_tasks()))


@app.route("/add", methods=["POST"])
def add_task():
    title       = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if not title:
        return redirect(url_for("index"))

    tasks = load_tasks()
    tasks.append({
        "id":          str(uuid.uuid4()),
        "title":       title,
        "description": description,
        "done":        False,
        "created_at":  datetime.now().strftime("%d %b %Y, %I:%M %p"),
    })
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    tasks = load_tasks()
    task  = find_task(tasks, task_id)
    if not task:
        return redirect(url_for("index"))

    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if title:
            task["title"]       = title
            task["description"] = description
            task["updated_at"]  = datetime.now().strftime("%d %b %Y, %I:%M %p")
            save_tasks(tasks)
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/toggle/<task_id>")
def toggle_task(task_id):
    tasks = load_tasks()
    task  = find_task(tasks, task_id)
    if task:
        task["done"] = not task["done"]
        save_tasks(tasks)
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
