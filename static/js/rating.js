/* jshint esversion: 6 */
// ------------------ Get cookie value by name

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ------------------ Highlight stars up to given value

function renderStars(stars, value) {
  stars.forEach((s, i) => {
    s.classList.toggle("rated", i < value);
    s.style.color = i < value ? "#f39c12" : "#ccc";
  });
}

// ------------------ Handle star rating UI and send rating via AJAX
// --- CHAPTER RATING ---
function initChapterRatings() {
  document.querySelectorAll(".rating-stars.chapter-rating").forEach((container) => {
    const stars = container.querySelectorAll(".star");
    const chapterId = container.getAttribute("data-chapter");
    let userRating = parseInt(container.getAttribute("data-user-rating")) || 0;

    // Set initial star colors
    renderStars(stars, userRating);

    stars.forEach((star, index) => {
      star.addEventListener("mouseenter", () => renderStars(stars, index + 1));
      star.addEventListener("mouseleave", () => renderStars(stars, userRating));
      star.addEventListener("click", () => {
        const value = parseInt(star.getAttribute("data-value"));

        fetch("/ajax/rate/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `chapter_id=${chapterId}&value=${value}`,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              userRating = value;
              container.setAttribute("data-user-rating", value);
              renderStars(stars, value);

              // Update average text if present
              const avgElem = container.parentElement.querySelector(".avg");
              if (avgElem) {
                avgElem.innerText = `(${data.average}/5) — ${data.count} user${data.count !== 1 ? "s" : ""} rated`;
              }
            } else {
              alert("Rating error: " + data.error);
            }
          })
          .catch((err) => {
            alert("Rating failed.");
          });
      });
    });
  });
}

// --- STORY RATING ---
function initStoryRatings() {
  document.querySelectorAll(".rating-stars.story-rating").forEach((container) => {
    const stars = container.querySelectorAll(".star");
    const storyId = container.getAttribute("data-story");
    let userRating = parseInt(container.getAttribute("data-user-rating")) || 0;

    // Set initial star colors
    renderStars(stars, userRating);

    stars.forEach((star, index) => {
      star.addEventListener("mouseenter", () => renderStars(stars, index + 1));
      star.addEventListener("mouseleave", () => renderStars(stars, userRating));
      star.addEventListener("click", () => {
        const value = parseInt(star.getAttribute("data-value"));

        fetch("/rate-story/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ story_id: storyId, rating: value }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.success) {
              userRating = value;
              container.setAttribute("data-user-rating", value);
              renderStars(stars, value);

              // Optionally, update any average display if you have it
              // Example:
              // const avgElem = container.parentElement.querySelector(".avg");
              // if (avgElem) {
              //   avgElem.innerText = `(${data.average}/5) — ${data.count} rated`;
              // }
            } else {
              alert("Rating error: " + data.error);
            }
          })
          .catch((err) => {
            alert("Something went wrong. Please try again.");
          });
      });
    });
  });
}

// --- READ-ONLY AVERAGE STARS ---
function renderAvgStars() {
  document.querySelectorAll(".avg-stars").forEach((container) => {
    const average = parseFloat(container.getAttribute("data-average")) || 0;
    const fullStars = Math.floor(average);
    let starsHTML = "";
    for (let i = 1; i <= 5; i++) {
      starsHTML += i <= fullStars ? "★" : "☆";
    }
    container.innerHTML = starsHTML;
    container.style.color = "#999";
    container.style.fontSize = "1.2rem";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initChapterRatings();
  initStoryRatings();
  renderAvgStars();
});
