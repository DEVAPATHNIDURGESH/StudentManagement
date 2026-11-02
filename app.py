
from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

from registration import registration_bp
from login import login_bp
from management import management_bp

app = Flask(__name__)
app.secret_key = "student_management_secret_key"

# Register blueprints
app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(management_bp)


# Database connection
def connect_db():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row
    return con


# Create or update database table
def init_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                password TEXT,
                department TEXT NOT NULL
            )
        """)

        columns = [
            row["name"]
            for row in con.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        ]

        if "email" not in columns:
            con.execute(
                "ALTER TABLE students ADD COLUMN email TEXT"
            )

        if "password" not in columns:
            con.execute(
                "ALTER TABLE students ADD COLUMN password TEXT"
            )


# READ - Display all students
@app.route("/")
def home():
    with connect_db() as con:
        students = con.execute(
            "SELECT * FROM students"
        ).fetchall()

    return render_template("index.html", students=students)


# CREATE - Add student
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        with connect_db() as con:
            con.execute(
                "INSERT INTO students (name, department) VALUES (?, ?)",
                (name, department)
            )

    return redirect("/")


# UPDATE - Update student
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        with connect_db() as con:
            con.execute(
                "UPDATE students SET name=?, department=? WHERE id=?",
                (name, department, id)
            )

    return redirect("/")


# DELETE - Delete student
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )

    return redirect("/")


# SEARCH - Search students by name
@app.route("/search")
def search():
    name = request.args.get("name", "").strip()

    with connect_db() as con:
        students = con.execute(
            """
            SELECT id, name, email, department
            FROM students
            WHERE name LIKE ?
            """,
            ("%" + name + "%",)
        ).fetchall()

    return jsonify([dict(student) for student in students])


# Run Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
