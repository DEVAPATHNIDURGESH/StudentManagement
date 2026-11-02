from flask import Blueprint, render_template, request, redirect
import sqlite3

management_bp = Blueprint("management", __name__)

def connect_db():
    return sqlite3.connect("students.db")

@management_bp.route("/students")
def students():
    with connect_db() as con:
        student_list = con.execute(
            "SELECT * FROM students"
        ).fetchall()

    return render_template("students.html", students=student_list)