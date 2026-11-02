from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

login_bp = Blueprint("login", __name__)

def connect_db():
    return sqlite3.connect("students.db")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"].strip()
        department = request.form["department"].strip()

        with connect_db() as con:
            student = con.execute(
                "SELECT * FROM students WHERE name=? AND department=?",
                (name, department)
            ).fetchone()

        if student:
            return redirect(url_for("home"))

        return "Invalid login details"

    return render_template("login.html")