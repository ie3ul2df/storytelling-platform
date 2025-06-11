document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).classList.add("d-none");
    document.getElementById(`edit-form-${id}`).classList.remove("d-none");
  });
});

document.querySelectorAll(".cancel-edit").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).classList.remove("d-none");
    document.getElementById(`edit-form-${id}`).classList.add("d-none");
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-comments-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const targetSelector = button.getAttribute("data-target");
      const target = document.querySelector(targetSelector);

      if (target) {
        const isHidden = target.classList.contains("d-none");
        target.classList.toggle("d-none");
        button.innerHTML = isHidden ? "💬 Hide Comments ▲" : "💬 Read Comments ▼";
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Handle edit button click
  document.querySelectorAll(".edit-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const commentId = btn.dataset.id;
      const form = document.getElementById(`edit-form-${commentId}`);
      const buttons = document.querySelector(`.edit-del-${commentId}`);
      if (form) form.classList.remove("d-none");
      if (buttons) buttons.classList.add("d-none");
    });
  });

  // Handle cancel button click
  document.querySelectorAll(".cancel-edit").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const commentId = btn.dataset.id;
      const form = document.getElementById(`edit-form-${commentId}`);
      const buttons = document.querySelector(`.edit-del-${commentId}`);
      if (form) form.classList.add("d-none");
      if (buttons) buttons.classList.remove("d-none");
    });
  });
});
