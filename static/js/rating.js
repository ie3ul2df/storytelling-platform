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

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".rating-stars").forEach((container) => {
    const stars = container.querySelectorAll(".star");
    const chapterId = container.getAttribute("data-chapter");

    // Set initial color on page load
    const userRating = parseInt(container.getAttribute("data-user-rating")) || 0;
    stars.forEach((s, i) => {
      s.style.color = i < userRating ? "#f39c12" : "#ccc";
    });

    stars.forEach((star, index) => {
      star.addEventListener("mouseenter", () => {
        stars.forEach((s, i) => {
          s.style.color = i <= index ? "#f39c12" : "#ccc";
        });
      });

      star.addEventListener("mouseleave", () => {
        const rated = parseInt(container.getAttribute("data-user-rating")) || 0;
        stars.forEach((s, i) => {
          s.style.color = i < rated ? "#f39c12" : "#ccc";
        });
      });

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
              container.setAttribute("data-user-rating", value);

              // Update star colors
              stars.forEach((s, i) => {
                s.style.color = i < value ? "#f39c12" : "#ccc";
              });

              // Safely update avg text
              const avgElem = container.querySelector(".avg") || container.parentElement.querySelector(".avg");
              if (avgElem) {
                avgElem.innerText = `(${data.average}/5) — ${data.count} user${data.count !== 1 ? "s" : ""} rated`;
              }
            } else {
              alert("Rating error: " + data.error);
            }
          })
          .catch((err) => {
            console.error("Rating failed:", err);
            alert("Rating failed.");
          });
      });
    });
  });
});

// Render readonly average stars
document.querySelectorAll(".avg-stars").forEach((container) => {
  const average = parseFloat(container.getAttribute("data-average"));
  const fullStars = Math.floor(average);
  const halfStar = average - fullStars >= 0.5;

  let starsHTML = "";
  for (let i = 1; i <= 5; i++) {
    if (i <= fullStars) {
      starsHTML += "★";
    } else {
      starsHTML += "☆";
    }
  }

  container.innerHTML = starsHTML;
  container.style.color = "#999";
  container.style.fontSize = "1.2rem";
});
