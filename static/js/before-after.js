// Before/after comparison slider.
// A native range input sits invisibly over the photos, so keyboard and screen-reader
// support come built in; this script just moves the divider to match its value.
document.querySelectorAll("[data-before-after]").forEach((slider) => {
    const range = slider.querySelector("[data-before-after-range]");
    if (!range) return;

    const update = () => {
        slider.style.setProperty("--position", `${range.value}%`);
    range.setAttribute("aria-valuetext", `${range.value}% before photo showing`);
    };

    range.addEventListener("input", update);
    update();
});