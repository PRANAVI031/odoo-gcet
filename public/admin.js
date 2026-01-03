const datePicker = document.getElementById("datePicker");
const adminData = document.getElementById("adminData");

datePicker.value = new Date().toISOString().split("T")[0];
loadHR();

datePicker.addEventListener("change", loadHR);

function loadHR() {
    const date = datePicker.value;

    fetch(`/admin/attendance/date/${date}?role=hr`)
        .then(r => {
            if (r.status === 403) {
                alert("HR access only ❌");
                window.location.href = "/";
                return;
            }
            return r.json();
        })
        .then(data => {
            if (!data) return;

            adminData.innerHTML = "";
            data.forEach(a => {
                adminData.innerHTML += `
                <tr>
                    <td>${a.employee_id}</td>
                    <td>${a.check_in || "-"}</td>
                    <td>${a.check_out || "-"}</td>
                    <td>${a.work_hours || "-"}</td>
                    <td>${a.extra_hours || "-"}</td>
                </tr>`;
            });
        });
}
