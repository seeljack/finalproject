// Add interactivity to project cards and navigation

document.addEventListener("DOMContentLoaded", () => {
  // Add hover effects to navigation links
  const navLinks = document.querySelectorAll("header nav ul li a");
  navLinks.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      link.style.transform = "scale(1.1)";
    });
    link.addEventListener("mouseleave", () => {
      link.style.transform = "scale(1)";
    });
  });

  // Add animations to project cards on hover
  const projectCards = document.querySelectorAll(".project");
  projectCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.boxShadow = "0 8px 15px rgba(0, 0, 0, 0.3)";
      card.style.transition = "box-shadow 0.3s ease";
    });
    card.addEventListener("mouseleave", () => {
      card.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
    });
  });

  // Add smooth scroll for the skip link
  const skipLink = document.querySelector(".skip-content");
  skipLink.addEventListener("click", (e) => {
    e.preventDefault();
    const target = document.querySelector(skipLink.getAttribute("href"));
    target.scrollIntoView({ behavior: "smooth" });
  });

  // Add dynamic project filters (example: filter by keyword)
  const projectsContainer = document.querySelector(".projects_container");
  const searchInput = document.createElement("input");
  searchInput.setAttribute("type", "text");
  searchInput.setAttribute("placeholder", "Search projects...");
  searchInput.style.margin = "20px auto";
  searchInput.style.display = "block";
  searchInput.style.padding = "10px";
  searchInput.style.width = "50%";
  searchInput.style.border = "1px solid #ddd";
  searchInput.style.borderRadius = "5px";

  document.querySelector("main").insertBefore(searchInput, projectsContainer);

  searchInput.addEventListener("input", () => {
    const filterText = searchInput.value.toLowerCase();
    projectCards.forEach((card) => {
      const title = card.querySelector("h2").textContent.toLowerCase();
      const description = card.querySelector("p").textContent.toLowerCase();

      if (title.includes(filterText) || description.includes(filterText)) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });
  });
});
