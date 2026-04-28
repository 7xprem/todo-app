# TaskFlow — To-Do App (Flask + JSON)

A full-featured To-Do web application built with **Python Flask** and **JSON file storage**.

---

## Features

| Feature | Details |
|---|---|
| ✅ Add Task | Title + optional description |
| ✏️ Edit Task | Update title & description |
| 🗑️ Delete Task | Removes task from file |
| ✔️ Toggle Done | Mark tasks complete/pending |
| 🔍 Search | Live search by title or description |
| 🔽 Filter | View All / Pending / Done |
| 💾 Persistent | All data saved in `tasks.json` |

---

## Project Structure

```
todo_app/
├── app.py              ← Flask routes + file handling logic
├── tasks.json          ← Auto-created on first task (persistent storage)
├── requirements.txt    ← Python dependencies
└── templates/
    ├── index.html      ← Main task list page
    └── edit.html       ← Edit task page
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## File Handling Logic

All task data is stored in **`tasks.json`** using Python's built-in `json` module.

### How it works:

- **`load_tasks()`** — Opens `tasks.json` and reads the list of task dictionaries using `json.load()`. Returns an empty list if the file doesn't exist yet.

- **`save_tasks(tasks)`** — Writes the entire updated list back to `tasks.json` using `json.dump()` with `indent=4` for human-readable formatting.

- **`find_task(tasks, task_id)`** — Searches the loaded list for a task matching a given UUID.

### Why JSON?
- Human-readable format (you can open `tasks.json` in any text editor)
- Structured data — each task is a dictionary with `id`, `title`, `description`, `done`, `created_at` fields
- Native Python support via the `json` module — no extra libraries needed

### Example `tasks.json` entry:
```json
[
    {
        "id": "a1b2c3d4-...",
        "title": "Submit assignment",
        "description": "Upload to portal before midnight",
        "done": false,
        "created_at": "29 Apr 2025, 10:30 AM"
    }
]
```

---

## CRUD Operations Summary

| Operation | Route | Method |
|---|---|---|
| **Create** | `/add` | POST |
| **Read** | `/` | GET |
| **Update** | `/edit/<id>` | GET + POST |
| **Delete** | `/delete/<id>` | GET |
| **Toggle** | `/toggle/<id>` | GET |
| **Search** | `/?q=keyword` | GET |
| **Filter** | `/?status=pending` | GET |
