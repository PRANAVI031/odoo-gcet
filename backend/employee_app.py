from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# ---------- DATABASE ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="leave_management",
        port=3306
    )

# ---------- UPLOAD CONFIG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- EMPLOYEE PAGE ----------
@app.route("/")
def employee_timeoff():
    employee = request.args.get("employee")  # simulate login

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM time_off_requests WHERE employee_name=%s ORDER BY created_at DESC",
        (employee,)
    )
    leaves = cur.fetchall()

    conn.close()

    return render_template(
        "employee_timeoff.html",
        leaves=leaves,
        employee_name=employee
    )

# ---------- APPLY LEAVE ----------
@app.route("/employee/apply", methods=["POST"])
def apply_leave():
    print("APPLY ROUTE HIT")
    print("FORM:", request.form)
    print("FILES:", request.files)

    attachment_name = None

    if "attachment" in request.files:
        file = request.files["attachment"]
        if file and file.filename != "":
            attachment_name = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, attachment_name))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO time_off_requests
        (employee_name, time_off_type, start_date, end_date, allocation_days, attachment)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        request.form.get("employee_name"),
        request.form.get("time_off_type"),
        request.form.get("start_date"),
        request.form.get("end_date"),
        request.form.get("allocation_days"),
        attachment_name
    ))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
