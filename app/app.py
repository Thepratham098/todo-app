from flask import Flask, request, jsonify, render_template, redirect, session
import psycopg2
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 Session security
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")
app.config['SESSION_PERMANENT'] = False

# ---------- DB CONNECTION ----------
def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ---------- CREATE TABLES ----------
@app.before_request
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium',
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER REFERENCES users(id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

# ---------- AUTH ----------

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'])

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (data['username'], hashed_password)
            )
            conn.commit()
        except:
            return "User already exists"

        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        data = request.form

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s",
            (data['username'],)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[2], data['password']):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    # Total tasks
    cur.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id=%s",
        (session['user_id'],)
    )
    total = cur.fetchone()[0]

    # Completed tasks
    cur.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id=%s AND completed=TRUE",
        (session['user_id'],)
    )
    completed = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        'profile.html',
        username=session.get('username'),
        total=total,
        completed=completed
    )

# ---------- TASKS ----------

@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, priority, user_id) VALUES (%s, %s, %s)",
        (data['title'], data.get('priority', 'Medium'), session['user_id'])
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Task added"})

@app.route('/tasks')
def get_tasks():
    if 'user_id' not in session:
        return jsonify([])

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, priority, completed, created_at
        FROM tasks
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (session['user_id'],))

    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "id": t[0],
            "title": t[1],
            "priority": t[2],
            "completed": t[3],
            "created_at": t[4].strftime("%Y-%m-%d %H:%M")
        }
        for t in tasks
    ])

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Deleted"})

@app.route('/complete/<int:id>', methods=['PUT'])
def complete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id=%s",
        (id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Updated"})

# ---------- RUN ----------

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.environ.get("PORT", 5000))  # 🌍 for Railway
    app.run(host="0.0.0.0", port=port)
=======
    port = int(os.environ.get("PORT", 5000))  # 🔥 Required for Render
    app.run(host="0.0.0.0", port=port)
>>>>>>> d9c2f12 (render ready app)
