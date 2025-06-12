/* jshint esversion: 6 */
// ------------------ Logs script load and defines function to get CSRF token from cookies

function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(";").forEach((c) => {
    const [k, v] = c.trim().split("=");
    if (k === name) cookieValue = decodeURIComponent(v);
  });
  return cookieValue;
}

// ------------------ Handles bookmark button clicks using AJAX and updates icon/title based on response

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".bookmark-btn");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const isBookmarked = btn.dataset.bookmarked === "true";
      const url = isBookmarked ? btn.dataset.unbookmarkUrl : btn.dataset.bookmarkUrl;

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((res) => {
          if (!res.ok) {
            return null;
          }
          return res.json();
        })
        .then((data) => {
          if (!data) return;
          const icon = btn.querySelector("i");
          if (data.bookmarked) {
            icon.classList.replace("bi-bookmark", "bi-bookmark-fill");
            btn.dataset.bookmarked = "true";
            btn.title = "Remove Bookmark";
          } else {
            icon.classList.replace("bi-bookmark-fill", "bi-bookmark");
            btn.dataset.bookmarked = "false";
            btn.title = "Bookmark";
          }
        })
        .catch((err) => console.error("Fetch failed:", err));
    });
  });
});
