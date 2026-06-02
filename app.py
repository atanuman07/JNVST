from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "jnvst_secret_key"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ADMISSION FORM
# =========================

@app.route("/admission", methods=["POST"])
def admission():

    name = request.form["name"]
    phone = request.form["phone"]
    student_class = request.form["student_class"]
    district = request.form["district"]

    conn = sqlite3.connect("admissions.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, phone, student_class, district)
        VALUES (?, ?, ?, ?)
    """, (name, phone, student_class, district))

    conn.commit()
    conn.close()

    return render_template("success.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect("/admin")

    return render_template("login.html")


# =========================
# ADMIN PANEL
# =========================

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("admissions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        students=students,
        total_students=total_students
    )

# =========================
# DELETE STUDENT
# =========================

@app.route("/delete/<int:id>")
def delete_student(id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("admissions.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")
# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )