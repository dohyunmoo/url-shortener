const urlForm = document.getElementById("long-url-form");
const urlInput = document.getElementById("long-url");
const shortUrlDisplay = document.getElementById("short-url");
const emojiUrlDisplay = document.getElementById("emoji-url");

urlForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const longUrl = urlInput.value;

    console.log(longUrl);

    if (validateUrl(longUrl)) {
        fetch("/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "long_url": longUrl })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                shortUrlDisplay.textContent = data.error;
                emojiUrlDisplay.textContent = data.error;
            } else {
                shortUrlDisplay.textContent = data.short_url;
                emojiUrlDisplay.textContent = data.emoji_code;
            }
        })
        .catch(error => console.error(error));
    } else {
        console.error("invalid URL");
    }
});

function validateUrl(urlString) {
    try {
        new URL(urlString);
        return true;
    } catch (error) {
        return false;
    }
}

const goButton = document.getElementById("go");
const shortenedUrl = document.getElementById("short-url");

goButton.addEventListener("click", () => {
    const mainUrl = "http://127.0.0.1:5000/";
    if (shortenedUrl.textContent != ""){
        console.log(mainUrl + shortenedUrl.textContent);
        window.location.replace(mainUrl + shortenedUrl.textContent);
    }
});

// const regenerateButton = document.getElementById("regen");

// regenerateButton.addEventListener("click", () => {

// });