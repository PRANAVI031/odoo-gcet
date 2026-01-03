const express = require("express");
const sqlite3 = require("sqlite3").verbose();

const app = express();
app.use(express.json());
app.use(express.static("public"));

const db = new sqlite3.Database("database.db");

// TABLE
db.run(`
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT,
    date TEXT,
    check_in TEXT,
    check_out TEXT,
    status TEXT
)
`);

// CHECK IN
app.post("/checkin", (req, res) => {
    const empId = req.body.empId;
    const date = new Date().toISOString().split("T")[0];
    const time = new Date().toLocaleTimeString();

    db.get(
        "SELECT * FROM attendance WHERE emp_id=? AND date=?",
        [empId, date],
        (err, row) => {
            if (row) return res.json({ message: "Already checked in" });

            db.run(
                "INSERT INTO attendance (emp_id, date, check_in, status) VALUES (?,?,?,?)",
                [empId, date, time, "Present"],
                () => res.json({ message: "Checked in" })
            );
        }
    );
});

// CHECK OUT
app.post("/checkout", (req, res) => {
    const empId = req.body.empId;
    const date = new Date().toISOString().split("T")[0];
    const time = new Date().toLocaleTimeString();

    db.run(
        "UPDATE attendance SET check_out=? WHERE emp_id=? AND date=?",
        [time, empId, date],
        () => res.json({ message: "Checked out" })
    );
});

// EMPLOYEE VIEW
app.get("/employee/:id", (req, res) => {
    db.all(
        "SELECT * FROM attendance WHERE emp_id=? ORDER BY date DESC",
        [req.params.id],
        (err, rows) => res.json(rows)
    );
});

// HR VIEW
app.get("/admin/attendance", (req, res) => {
    const date = req.query.date;
    db.all(
        "SELECT * FROM attendance WHERE date=?",
        [date],
        (err, rows) => res.json(rows)
    );
});

app.listen(3000, () => {
    console.log("Server running at http://localhost:3000");
});
