function openPopup() {
  document.getElementById("popup").style.display = "block";
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

function calculateDays() {
  const start = document.getElementById("start_date").value;
  const end = document.getElementById("end_date").value;

  if (start && end) {
    const s = new Date(start);
    const e = new Date(end);

    if (e >= s) {
      const diffDays =
        Math.floor((e - s) / (1000 * 60 * 60 * 24)) + 1;
      document.getElementById("allocation_days").value = diffDays;
    } else {
      document.getElementById("allocation_days").value = "";
    }
  }
}

function openPopup() {
  document.getElementById("popup").style.display = "block";
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

function calculateDays() {
  const start = document.getElementById("start_date").value;
  const end = document.getElementById("end_date").value;

  if (start && end) {
    const s = new Date(start);
    const e = new Date(end);

    if (e >= s) {
      document.getElementById("allocation_days").value =
        Math.floor((e - s) / (1000 * 60 * 60 * 24)) + 1;
    }
  }
}

function submitLeave() {

  const formData = new FormData();
  formData.append("employee_name", document.getElementById("employee_name").value);
  formData.append("time_off_type", document.getElementById("time_off_type").value);
  formData.append("start_date", document.getElementById("start_date").value);
  formData.append("end_date", document.getElementById("end_date").value);
  formData.append("allocation_days", document.getElementById("allocation_days").value);

  const fileInput = document.getElementById("attachment");
  if (fileInput.files.length > 0) {
    formData.append("attachment", fileInput.files[0]);
  }

  fetch("/employee/apply", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(() => {
    window.location.href =
      "/?employee=" + encodeURIComponent(document.getElementById("employee_name").value);
  })
  .catch(err => console.error(err));
}

