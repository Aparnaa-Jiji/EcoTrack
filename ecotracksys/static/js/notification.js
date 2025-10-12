// ecotracksys/static/js/notifications.js

// Toast popup function
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.innerText = message;
  toast.style.position = "fixed";
  toast.style.bottom = "20px";
  toast.style.right = "20px";
  toast.style.background = type === "error" ? "#d32f2f" : "#1976d2"; // red for error, blue for success
  toast.style.color = "white";
  toast.style.padding = "10px 15px";
  toast.style.borderRadius = "6px";
  toast.style.boxShadow = "0 4px 8px rgba(0,0,0,0.3)";
  toast.style.zIndex = "9999";
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 2500);
}

// Toggle Read/Unread
function toggleRead(id, csrfToken) {
  fetch(`/api/notifications/${id}/toggle_read/`, {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken }
  })
    .then(res => res.json())
    .then(data => {
      showToast(data.msg);
      setTimeout(() => location.reload(), 1000);
    })
    .catch(() => showToast("Something went wrong", "error"));
}

// Delete Notification
function deleteNotif(id, csrfToken) {
  fetch(`/api/notifications/${id}/delete/`, {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken }
  })
    .then(res => res.json())
    .then(data => {
      showToast(data.msg);
      setTimeout(() => location.reload(), 1000);
    })
    .catch(() => showToast("Something went wrong", "error"));
}
