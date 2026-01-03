from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from flask_cors import CORS

from utils import generate_login_id

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = "dayflow_secret_123"

# ENABLE CORS (IMPORTANT FOR FRONTEND DASHBOARD)
CORS(app)

# -------- DATABASE ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dayflow"
)

# -------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE login_id=%s OR email=%s",
            (identifier, identifier)
        )
        user = cursor.fetchone()

        if not user:
            flash("User not found", "error")
            return redirect("/")

        if not pbkdf2_sha256.verify(password, user["password_hash"]):
            flash("Wrong password!", "error")
            return redirect("/")

        session["user"] = user["login_id"]
        flash("Login Successful", "success")
        return redirect("/dashboard")

    return render_template("signin.html")

# -------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        company_name = request.form["company"]
        first_name = request.form["first"]
        last_name = request.form["last"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        cursor = db.cursor()

        try:
            login_id = generate_login_id(company_name, first_name, last_name, db)
            password_hash = pbkdf2_sha256.hash(password)

            cursor.execute("""
                INSERT INTO users
                (login_id, company_name, first_name, last_name, email, phone,
                 password_hash, role, joining_date)
                VALUES (%s,%s,%s,%s,%s,%s,%s,'Admin',%s)
            """, (
                login_id,
                company_name,
                first_name,
                last_name,
                email,
                phone,
                password_hash,
                datetime.now()
            ))

            db.commit()

            return render_template("signup.html", login_id=login_id)

        except Exception as e:
            print(e)
            flash("Email already exists!", "error")
            return render_template("signup.html")

    return render_template("signup.html")


# -------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return f"Welcome {session['user']} — Dashboard Coming Soon 😊"

# -------- API : EMPLOYEES (FOR YOUR DASHBOARD) ----------
@app.route("/api/employees", methods=["GET"])
def api_employees():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            id,
            first_name,
            last_name,
            role
        FROM users
    """)
    rows = cursor.fetchall()

    employees = []
    for r in rows:
        employees.append({
            "id": r["id"],
            "name": f"{r['first_name']} {r['last_name']}",
            "designation": r["role"],
            "status": "PRESENT"   # default demo status
        })

    return employees

# -------- FORGOT PASSWORD ----------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        flash("OTP sent to your email! (Demo only)", "success")
        return redirect("/verify-otp")

    return render_template("forgot_password.html")

# -------- VERIFY OTP ----------
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        otp = request.form["otp"]

        if otp == "123456":
            flash("OTP Verified!", "success")
            return redirect("/reset-password")

        flash("Invalid OTP!", "error")
        return redirect("/verify-otp")

    return render_template("verify_otp.html")

# -------- RESET PASSWORD ----------
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect("/reset-password")

        flash("Password reset successful! (Demo only)", "success")
        return redirect("/")

    return render_template("reset_password.html")

# -------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)