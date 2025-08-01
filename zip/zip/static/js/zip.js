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

function setupMobileMenuToggle() {
  const menuButton = document.querySelector(".page-header #menu-button");
  const navLinks = document.querySelector(".page-header .nav-links");

  menuButton.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });
}

function setupFilters() {
  const sectionFilters = document.querySelectorAll(".section-filters");

  sectionFilters.forEach((filterSection) => {
    const filterParents = filterSection.hasAttribute("data-key")
      ? [filterSection]
      : filterSection.querySelectorAll("[data-key]");
    if (filterParents.length === 0) return;

    filterParents.forEach((filterParent) => {
      const filterKey = filterParent.getAttribute("data-key");
      const filterIsRange =
        filterParent.hasAttribute("data-range") &&
        filterParent.getAttribute("data-range") !== "false";
      const filterPills = filterParent.querySelectorAll(".filter-pill");
      const filterSelect = filterParent.querySelector("select");
      const filterItems = filterSection.nextElementSibling.querySelectorAll(
        `[data-${filterKey}]`
      );

      const updateItemsDisplay = (filterValue) => {
        filterItems.forEach((item) => {
          const itemValue = item.dataset[filterKey];
          if (filterIsRange) {
            const filterValueNum = Number(filterValue);
            const itemValueNums = itemValue.split("-").map(Number);
            if (
              filterValue === "all" ||
              (itemValueNums.length === 2 &&
                itemValueNums[0] <= filterValueNum &&
                itemValueNums[1] >= filterValueNum)
            ) {
              item.style.display = "";
            } else {
              item.style.display = "none";
            }
          } else {
            if (filterValue === "all" || itemValue === filterValue) {
              item.style.display = "";
            } else {
              item.style.display = "none";
            }
          }
        });
      };

      if (filterPills.length) {
        filterPills.forEach((filterPill) => {
          const filterValue = filterPill.getAttribute("data-filter");
          filterPill.addEventListener("click", (event) => {
            event.preventDefault();

            filterPills.forEach((pill) => pill.classList.remove("active"));
            filterPill.classList.add("active");

            updateItemsDisplay(filterValue);
          });
        });
      }

      if (filterSelect) {
        const allOption = filterSelect.querySelector("option[value='all']");

        let selectedValue = (() => {
          const opt = filterSelect.querySelector("option:checked");
          return opt ? opt.value : "all";
        })();

        const updateAllOptionText = () => {
          if (allOption) {
            if (selectedValue === "all") {
              allOption.setAttribute("disabled", "disabled");
              allOption.textContent = allOption.dataset.selectText;
            } else {
              allOption.removeAttribute("disabled");
              allOption.textContent = allOption.dataset.allText;
            }
          }
        };
        updateAllOptionText();
        updateItemsDisplay(selectedValue);

        filterSelect.addEventListener("change", (event) => {
          if (selectedValue !== event.target.value) {
            selectedValue = event.target.value;
          }
          updateAllOptionText();

          updateItemsDisplay(selectedValue);
        });
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupGalleries();
  setupClickableNewsItems();
  setupMobileMenuToggle();
  setupFilters();
});
