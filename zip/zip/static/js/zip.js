function setupGalleries() {
  document.querySelectorAll(".gallery__items").forEach((galleryItems) => {
    const largeImageContainer = galleryItems.querySelector(".gallery__image");
    const largeImage = largeImageContainer.querySelector("img");
    const rollList = galleryItems.querySelector(".gallery__roll ul");
    const rollImages = rollList.querySelectorAll("li a");

    const prev = galleryItems.querySelector(".gallery__roll .prev");
    const next = galleryItems.querySelector(".gallery__roll .next");

    function onRollImageClick(event, roll) {
      event.preventDefault();

      const activeRollImage = rollList.querySelector("li a.active");
      activeRollImage.classList.remove("active");

      largeImage.setAttribute("src", roll.getAttribute("data-large-url"));
      largeImage.setAttribute("width", roll.getAttribute("data-large-width"));
      largeImage.setAttribute("height", roll.getAttribute("data-large-height"));

      roll.classList.add("active");

      const offset =
        roll.offsetLeft -
        rollList.offsetLeft -
        (rollList.offsetWidth / 2 - roll.offsetWidth / 2);
      rollList.scrollTo({ left: offset, behavior: "smooth" });
    }

    rollImages.forEach((rollImage) => {
      rollImage.addEventListener("click", (event) =>
        onRollImageClick(event, rollImage)
      );
    });

    prev.addEventListener("click", (event) => {
      const activeRollImage = rollList.querySelector("li a.active");
      const prevRoll = activeRollImage.parentElement.previousElementSibling;
      const prevRollImage = prevRoll?.querySelector("a");
      if (prevRollImage) {
        onRollImageClick(event, prevRollImage);
      }
    });

    next.addEventListener("click", (event) => {
      const activeRollImage = rollList.querySelector("li a.active");
      const nextRoll = activeRollImage.parentElement.nextElementSibling;
      const nextRollImage = nextRoll?.querySelector("a");
      if (nextRollImage) {
        onRollImageClick(event, nextRollImage);
      }
    });
  });
}

function setupClickableNewsItems() {
  const setupClickHandler = (item) => {
    item.style.cursor = "pointer";
    item.addEventListener("click", (event) => {
      // Don't navigate if text is selected
      const selectedText = window.getSelection().toString();
      if (selectedText) return;

      if (!event.target.closest("a")) {
        const link = item.querySelector(".js-item-link");
        if (link) {
          link.click();
        }
      }
    });
  };

  document.querySelectorAll(".js-news-item").forEach(setupClickHandler);
}

document.addEventListener("DOMContentLoaded", () => {
  setupGalleries();
  setupClickableNewsItems();
});
