document.getElementById("summarize-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let urlInput = document.getElementById("url").value;
    if (!urlInput.startsWith("http")) {
        urlInput = "https://" + urlInput;
    }

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ "url": urlInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("website-title").innerText = data.title;

        // Convert Markdown to HTML using marked.js
        document.getElementById("summary-content").innerHTML = marked.parse(data.summary);

        document.getElementById("result").classList.remove("hidden");
    })
    .catch(error => console.error("Error:", error));
});
