document.addEventListener("DOMContentLoaded", function () {

    const logo = document.getElementById("logo");
    const heading = document.querySelector("h1");

    // Logo click
    if (logo) {
        logo.addEventListener("click", function () {
            alert("Sameer Electronics - Library System");
        });

        // Hover effect
        logo.addEventListener("mouseover", () => {
            logo.style.transform = "scale(1.1)";
            logo.style.transition = "0.3s";
        });

        logo.addEventListener("mouseout", () => {
            logo.style.transform = "scale(1)";
        });
    }

    // Heading style
    if (heading) {
        heading.style.color = "#0a3d62";
        heading.style.textAlign = "center";
    }

    console.log("Page Loaded");
});
