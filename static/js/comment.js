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
