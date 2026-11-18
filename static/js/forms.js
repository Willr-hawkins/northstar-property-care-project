// Prevent accidental double submits: disable the submit button once the form is sent.
document.querySelectorAll("form[data-submit-once]").forEach((form) => {
    const button = form.querySelector('[type="submit"]');
    if (!button) return;
    const orignalLabel = button.textContent;

    form.addEventListener("submit", () => {
        // Wait a tick so the browser has started the submission before the button is disabled.
        setTimeout(() => {
            button.disabled = true;
            button.textContent = button.dataset.sendingLabel || "Sending...";
        }, 0);
    });


    // Back/Forward navigation can restore the page with the button still disabled.
    window.addEventListener("pageshow", (event) => {
        if (event.persisted) {
            button.disabled = false;
            button.textContent = orignalLabel;
        }
    });
});