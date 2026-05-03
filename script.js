function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");

    menu.classList.toggle("open")
    icon.classList.toggle("open")

}

let cachedThemeIcons = null;
function getThemeIcons() {
    if (!cachedThemeIcons) {
        cachedThemeIcons = document.querySelectorAll(".theme-btn");
    }
    return cachedThemeIcons;
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");

    const icons = getThemeIcons();
    icons.forEach(icon => {
        icon.innerHTML = isDark ? "☀️" : "🌙";
    });

    localStorage.setItem("theme", isDark ? "dark" : "light");
}

window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        getThemeIcons().forEach(icon => {
            icon.innerHTML = "☀️";
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    });

    const hiddenElements = document.querySelectorAll('.hidden');
    hiddenElements.forEach((el) => observer.observe(el));
});
