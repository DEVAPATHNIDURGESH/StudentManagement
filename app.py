from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
# Database connection
def connect_db():
    return sqlite3.connect("students.db")
# Create table
with connect_db() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)
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
                "INSERT INTO students (name, department) VALUES (?, ?)", (name, department)
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
                "UPDATE students SET name=?, department=? WHERE 		id=?",
                (name, department, id)
            )

    return redirect("/")
# DELETE - Delete student
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM students WHERE id=?", (id,)
        )
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port = 5001)