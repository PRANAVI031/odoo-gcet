from flask import Flask, render_template, request, jsonify, send_from_directory
import mysql.connector
import os

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

# ---------- SERVE UPLOADED FILES ----------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/")
def admin_timeoff():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM time_off_requests ORDER BY created_at DESC")
    leaves = cur.fetchall()
    conn.close()
    return render_template("admin_timeoff.html", leaves=leaves)

@app.route("/admin/update", methods=["POST"])
def update_status():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE time_off_requests SET status=%s WHERE id=%s",
        (data["status"], data["id"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Status Updated"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
