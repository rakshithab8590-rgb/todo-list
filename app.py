from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_db():
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        cursor_factory=RealDictCursor,
        sslmode="require"
    )
    return conn


# ─── CREATE TABLE IF NOT EXISTS (runs on startup) ─────────────────
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# Run database initialization
with app.app_context():
    init_db()


# ─── ROUTES ──────────────────────────────────────────────────────

# Home - show all todos
@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
    todos = cur.fetchall()
    cur.close()
    conn.close()

    total = len(todos)
    done_count = sum(1 for t in todos if t['done'])
    pending = total - done_count

    return render_template(
        "index.html",
        todos=todos,
        total=total,
        done_count=done_count,
        pending=pending
    )


# Add a new todo
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()
    if task:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("index"))


# Toggle done/not done
@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET done = NOT done WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


# Delete a todo
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


# Delete all completed todos
@app.route("/clear-done")
def clear_done():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE done = TRUE")
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


# ─── START ────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)