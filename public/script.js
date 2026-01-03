const empInput = document.getElementById("empId");
const tableBody = document.getElementById("attendanceData");

document.getElementById("checkInBtn").onclick = () => {
    if (!empInput.value) return alert("Enter Employee ID");

    fetch("/checkin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ empId: empInput.value })
    }).then(loadAttendance);
};

document.getElementById("checkOutBtn").onclick = () => {
    if (!empInput.value) return alert("Enter Employee ID");

    fetch("/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ empId: empInput.value })
    }).then(loadAttendance);
};

function loadAttendance() {
    fetch(`/employee/${empInput.value}`)
        .then(res => res.json())
        .then(rows => {
            tableBody.innerHTML = "";
            rows.forEach(r => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${r.date}</td>
                        <td>${r.check_in || "-"}</td>
                        <td>${r.check_out || "-"}</td>
                        <td>${r.status}</td>
                    </tr>
                `;
            });
        });
}
