// Scroll reveal: adds .is-revealed to [data-reveal] elements as they enter the viewport.
(function () {
    window.northstarReveal = true; // tells the <head> safety net this script loaded

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const supported = "IntersectionObserver" in window;

    const observer = supported && !reduceMotion
        ? new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add("is-revealed");
                observer.unobserve(entry.target);
            });
        }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 })
        : null;

    function scan(root) {
        const items = root.matches?.("[data-reveal]") ? [root] : [];
        items.push(...root.querySelectorAll("[data-reveal"));
        items.forEach((el) => (observer ? observer.observe(el) : el.classList.add("is-revealed")));
    }

    scan(document);
    // Content swapped in by HTMX (e.g. the projects filter) needs observing too.
    document.addEventListener("htmx:load", (event) => scan(event.detail.elt));
})(); 