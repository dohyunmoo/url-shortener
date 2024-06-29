const form = document.getElementById("long-url-form");
const urlInput = document.getElementById("long-url");
const shortUrlDisplay = document.getElementById("short-url");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const longUrl = urlInput.value;

    console.log(longUrl);

    fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "long_url": longUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            shortUrlDisplay.textContent = data.error;
        } else {
            shortUrlDisplay.textContent = data.short_url;
        }
    })
    .catch(error => console.error(error));
});
