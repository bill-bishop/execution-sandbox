// ==UserScript==
// @name         Auto Confirm Button Clicker
// @namespace    http://tampermonkey.net/
// @version      1.6
// @description  Debugging mutation observer by simulating DOM changes.
// @author       Your Name
// @match        https://*.chatgpt.com/*
// @match        file:///*/test-confirm-trigger.html
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    console.log('Script initialized for debugging.');

    // Debugging mutation observer
    const observer = new MutationObserver((mutations) => {
        console.log('Mutations detected:', mutations);
        for (const mutation of mutations) {
            const confirmButton = Array.from(document.querySelectorAll('article button'))
                .find(btn => btn.textContent.trim().toLowerCase() === 'confirm');
            if (confirmButton) {
                console.log('Confirm button found:', confirmButton);
                confirmButton.click();
                console.log('Confirm button clicked successfully!');
                observer.disconnect();
                return;
            }
        }
    });

    // Start observing
    observer.observe(document.body, { childList: true, subtree: true });

    // Simulate a mutation for debugging
    setTimeout(() => {
        const article = document.createElement('article');
        const button = document.createElement('button');
        button.textContent = 'Confirm';
        article.appendChild(button);
        document.body.appendChild(article);
        console.log('Simulated button added to DOM.');
    }, 2000);
})();