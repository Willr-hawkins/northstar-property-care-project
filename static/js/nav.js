// Mobile navigation toggle — the only custom JS on the public site.
(function () {
    const toggle = document.querySelector("[data-nav-toggle]");
    const menu = document.getElementById("mobile-nav");
    if (!toggle || !menu) return;
  
    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      menu.hidden = !open;
    }
  
    toggle.addEventListener("click", () => {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
  
    // Escape closes the menu and returns focus to the toggle
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
  
    // Close if the viewport grows past the mobile breakpoint
    window.matchMedia("(min-width: 48rem)").addEventListener("change", (e) => {
      if (e.matches) setOpen(false);
    });
  })();