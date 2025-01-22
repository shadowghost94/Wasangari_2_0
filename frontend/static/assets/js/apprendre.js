document.querySelectorAll(".question-summary").forEach((item) => {
    item.addEventListener("click", () => {
        const detail = item.nextElementSibling;
        const icon = item.querySelector(".fas");

        if (detail.style.display === "block") {
            detail.style.display = "none";
            icon.classList.remove("fa-chevron-up");
            icon.classList.add("fa-chevron-down");
        } else {
            detail.style.display = "block";
            icon.classList.remove("fa-chevron-down");
            icon.classList.add("fa-chevron-up");
        }
    });
});
