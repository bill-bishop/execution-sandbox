// ==UserScript==
// @name         Auto Next Steps Helper
// @namespace    http://tampermonkey.net/
// @version      2.9
// @description  Watches for articles with 'MY NEXT STEPS' in their last <p> tag, updates the prompt, and clicks the send button after ensuring readiness. Debounces the main mutation observer to prevent excessive firing.
// @author       Your Name
// @match        https://*.chatgpt.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    console.log('Auto Next Steps Helper Script Initialized');

    // Regex to match 'MY NEXT STEPS' in the last <p> tag
    const formatRegex = /^MY NEXT STEPS/;
    let responseTimeout = null;
    let observerDebounceTimeout = null;
    let currentArticleObserver = null;

    // Function to clear any pending response timeout
    function clearPendingTimeout() {
        if (responseTimeout) {
            clearTimeout(responseTimeout);
            responseTimeout = null;
            console.log('Pending response timeout cleared.');
        }
    }

    // Function to handle next steps
    function handleNextSteps() {
        const promptDiv = document.querySelector('#prompt-textarea');

        if (promptDiv) {
            promptDiv.innerHTML = '<p>Go ahead and continue with your next steps</p>';
            promptDiv.dispatchEvent(new Event('input', { bubbles: true }));
            console.log('Prompt updated. Waiting for send button.');

            // Wait for the send button to appear after prompt update
            const waitForSendButton = setInterval(() => {
                const sendButton = document.querySelector('button[data-testid="send-button"]');
                if (sendButton && !sendButton.disabled) {
                    clearInterval(waitForSendButton);
                    sendButton.click();
                    console.log('Send button clicked.');
                }
            }, 500); // Check every 500ms
        } else {
            console.log('Prompt div not ready yet. Waiting.');
        }
    }

    // Observe a single article for mutations
    function observeLastArticle(articleNode) {
        console.log('Observing last article for mutations:', articleNode);

        // Disconnect the current observer if it exists
        if (currentArticleObserver) {
            currentArticleObserver.disconnect();
            console.log('Disconnected previous article observer.');
        }

        const observer = new MutationObserver((mutations) => {
            clearPendingTimeout();

            const lastParagraph = Array.from(articleNode.querySelectorAll('p')).pop();
            const lastLine = lastParagraph ? lastParagraph.textContent.trim() : '';
            console.log(`Last <p> content of article: '${lastLine}'`);

            const sendButton = document.querySelector('button[data-testid="send-button"]');
            const speechButton = document.querySelector('button[data-testid="composer-speech-button"]');

            if (
                formatRegex.test(lastLine) &&
                (!sendButton || !sendButton.disabled) &&
                (!speechButton || !speechButton.disabled)
            ) {
                console.log('Conditions met for MY NEXT STEPS response. Setting debounce timeout.');
                responseTimeout = setTimeout(() => {
                    handleNextSteps();
                }, 10000); // Debounce timeout (10 seconds)
            }
        });

        observer.observe(articleNode, { childList: true, subtree: true, characterData: true });
        currentArticleObserver = observer; // Save the current observer
    }

    // Main observer for the 'main' element to track articles
    const mainElement = document.querySelector('main');
    if (mainElement) {
        const observer = new MutationObserver((mutations) => {
            if (observerDebounceTimeout) {
                clearTimeout(observerDebounceTimeout);
            }

            observerDebounceTimeout = setTimeout(() => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1 && node.tagName === 'ARTICLE') {
                            console.log('New article detected in main. Observing.');
                            observeLastArticle(node);
                        }
                    });
                });
            }, 2000); // Debounce timeout for main observer
        });

        observer.observe(mainElement, { childList: true, subtree: true });
        console.log('Main observer set up to watch for new articles inside main.');

        // Observe the last article already on the page
        const lastArticle = Array.from(mainElement.querySelectorAll('article')).pop();
        if (lastArticle) {
            console.log('Observing last article on initialization inside main.');
            observeLastArticle(lastArticle);
        }
    } else {
        console.log('Main element not found. Observer not initialized.');
    }
})();