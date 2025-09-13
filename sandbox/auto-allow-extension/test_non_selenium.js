const { JSDOM } = require('jsdom');

// Simulate a browser-like environment
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, { url: "https://chatgpt.com" });
const { document } = dom.window;

console.log("Non-Selenium Test: Starting environment setup.");

// Add a MutationObserver to the document
const observer = new dom.window.MutationObserver((mutations) => {
    console.log("Mutation observed:", mutations);
    const confirmButton = document.querySelector("article button");
    if (confirmButton && confirmButton.textContent.trim().toLowerCase() === "confirm") {
        console.log("Confirm button found and clicked:", confirmButton.outerHTML);
        confirmButton.setAttribute("data-clicked", "true"); // Simulate click
    }
});
observer.observe(document.body, { childList: true, subtree: true });

// Simulate adding a button after some time
setTimeout(() => {
    const article = document.createElement("article");
    const button = document.createElement("button");
    button.textContent = "Confirm";
    article.appendChild(button);
    document.body.appendChild(article);
    console.log("Simulated button added to DOM:", button.outerHTML);
}, 1000);

// Check results after the simulation
setTimeout(() => {
    const clickedButton = document.querySelector("article button[data-clicked='true']");
    if (clickedButton) {
        console.log("Test Passed: Button was successfully clicked.");
    } else {
        console.log("Test Failed: Button was not clicked.");
    }
    observer.disconnect();
}, 2000);