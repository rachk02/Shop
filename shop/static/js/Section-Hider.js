document.addEventListener("DOMContentLoaded", function() {
      const descriptionContainer = document.getElementById("description-container");
      const toggleButton = document.getElementById("toggle-button");

      toggleButton.addEventListener("click", function() {
        descriptionContainer.classList.toggle("hidden");
      });
    });