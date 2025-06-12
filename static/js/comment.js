/* jshint esversion: 6 */
/* global bootstrap */

// ------------------ Shows comment edit form and hides original text when edit button is clicked

document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).classList.add("d-none");
    document.getElementById(`edit-form-${id}`).classList.remove("d-none");
  });
});

// ------------------ Cancel edit: show text, hide form

document.querySelectorAll(".cancel-edit").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).classList.remove("d-none");
    document.getElementById(`edit-form-${id}`).classList.add("d-none");
  });
});

// ------------------ Toggle comment section visibility and button text

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

// ------------------ Toggle comment edit form and buttons on edit/cancel

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

// ------------------ Initialize all Bootstrap carousels on the page

document.querySelectorAll(".carousel").forEach((el) => {
  new bootstrap.Carousel(el); // jshint ignore:line
});
