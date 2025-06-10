document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).style.display = "none";
    document.getElementById(`edit-form-${id}`).style.display = "block";
  });
});

document.querySelectorAll(".cancel-edit").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.id;
    document.getElementById(`comment-text-${id}`).style.display = "block";
    document.getElementById(`edit-form-${id}`).style.display = "none";
  });
});
