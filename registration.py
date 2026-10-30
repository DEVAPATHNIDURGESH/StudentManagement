
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

registration_bp = Blueprint("registration", __name__)

def connect_db():
    return sqlite3.connect("students.db")

@registration_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        department = request.form["department"].strip()

        if name and department:
            with connect_db() as con:
                con.execute(
                    "INSERT INTO students (name, department) VALUES (?, ?)",
                    (name, department)
                )

            return redirect(url_for("home"))

    return render_template("register.html")
