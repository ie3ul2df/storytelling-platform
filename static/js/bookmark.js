// ------------------ Logs script load and defines function to get CSRF token from cookies
console.log("✅ bookmark.js loaded");

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
  console.log(`Found ${buttons.length} .bookmark-btn(s)`);
  buttons.forEach((btn) => {
    console.log("Attaching click to story", btn.dataset.storyId);
    btn.addEventListener("click", () => {
      const isBookmarked = btn.dataset.bookmarked === "true";
      const url = isBookmarked ? btn.dataset.unbookmarkUrl : btn.dataset.bookmarkUrl;
      console.log(`→ ${isBookmarked ? "Unbookmarking" : "Bookmarking"} via`, url);

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((res) => {
          if (!res.ok) {
            console.error("Network error:", res.status, res.statusText);
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
