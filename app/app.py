from flask import Flask, request, jsonify, render_template, redirect, session
import psycopg2
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 Session security
app.config['SECRET_KEY'] = str(time.time())
app.config['SESSION_PERMANENT'] = False

# ---------- DB ----------
def get_db_connection():
    while True:
        try:
            return psycopg2.connect(
                host="db",
                database="todo_db",
                user="postgres",
                password="postgres"
            )
        except:
            print("Waiting for DB...")
            time.sleep(2)

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
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed = generate_password_hash(data['password'])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username,password) VALUES (%s,%s)",
                    (data['username'], hashed))

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    session.clear()

    if request.method == 'POST':
        data = request.form

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=%s",(data['username'],))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[2], data['password']):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
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

    one_week = datetime.now() - timedelta(days=7)

    # Total tasks
    cur.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id=%s AND created_at >= %s
    """, (session['user_id'], one_week))
    total = cur.fetchone()[0]

    # Completed tasks
    cur.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id=%s AND completed=TRUE AND created_at >= %s
    """, (session['user_id'], one_week))
    completed = cur.fetchone()[0]

    # 📊 Tasks per day (last 7 days)
    cur.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM tasks
        WHERE user_id=%s AND created_at >= %s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (session['user_id'], one_week))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Format for chart
    dates = []
    counts = []

    for r in rows:
        dates.append(r[0].strftime("%d %b"))
        counts.append(r[1])

    return render_template(
        'profile.html',
        total=total,
        completed=completed,
        dates=dates,
        counts=counts
    )

# ---------- TASKS ----------
@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({"error":"Unauthorized"}),401

    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (title, priority, user_id)
        VALUES (%s,%s,%s)
    """,(data['title'], data['priority'], session['user_id']))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg":"added"})

@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return jsonify([])

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,title,priority,completed,created_at
        FROM tasks
        WHERE user_id=%s
        ORDER BY created_at DESC
    """,(session['user_id'],))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "id":t[0],
            "title":t[1],
            "priority":t[2],
            "completed":t[3],
            "created_at":t[4].strftime("%Y-%m-%d %H:%M")
        } for t in data
    ])

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=%s",(id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg":"deleted"})

@app.route('/complete/<int:id>', methods=['PUT'])
def complete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE tasks SET completed=NOT completed WHERE id=%s",(id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg":"updated"})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)