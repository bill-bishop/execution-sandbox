// ==UserScript==
// @name         Functional Next Steps Helper
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Reimagined script for handling 'MY NEXT STEPS' functionality with an event-driven, functional flow.
// @author       Your Name
// @match        https://*.chatgpt.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    console.log('Functional Next Steps Helper Script Initialized');

    // Utility: Wait for an element to appear
    function waitForElement(selector, timeout = 10000) {
        return new Promise((resolve, reject) => {
            const interval = 100;
            let elapsed = 0;

            const check = setInterval(() => {
                const element = document.querySelector(selector);
                if (element) {
                    clearInterval(check);
                    resolve(element);
                }

                elapsed += interval;
                if (elapsed >= timeout) {
                    clearInterval(check);
                    reject(new Error(`Element ${selector} not found within ${timeout}ms.`));
                }
            }, interval);
        });
    }

    // Step 1: Monitor for new articles
    async function monitorForArticles() {
        console.log('Step 1: Monitoring for new articles.');

        const mainElement = await waitForElement('main');
        const observer = new MutationObserver(async (mutations) => {
            for (const mutation of mutations) {
                for (const node of mutation.addedNodes) {
                    if (node.nodeType === 1 && node.tagName === 'ARTICLE') {
                        console.log('New article detected. Processing.');
                        await processArticle(node);
                    }
                }
            }
        });

        observer.observe(mainElement, { childList: true, subtree: false });
    }

    // Step 2: Process an article
    async function processArticle(articleNode) {
        console.log('Step 2: Processing article:', articleNode);

        // Wait for the article to stabilize
        await waitForStabilization(articleNode);

        // Extract the last <p> tag
        const lastParagraph = Array.from(articleNode.querySelectorAll('p')).pop();
        if (!lastParagraph) {
            console.log('No <p> tags found in the article. Skipping.');
            return;
        }

        const lastLine = lastParagraph.textContent.trim();
        console.log(`Last line of article: '${lastLine}'`);

        if (/^MY NEXT STEPS/.test(lastLine)) {
            console.log('Conditions met for MY NEXT STEPS. Proceeding to next step.');
            await triggerNextSteps();
        }
    }

    // Step 3: Wait for article stabilization (text updates to stop)
    async function waitForStabilization(articleNode, timeout = 10000) {
        console.log('Step 3: Waiting for article stabilization.');

        return new Promise((resolve) => {
            let previousText = articleNode.textContent.trim();
            let elapsed = 0;
            const interval = 500;

            const check = setInterval(() => {
                const currentText = articleNode.textContent.trim();
                if (currentText === previousText) {
                    clearInterval(check);
                    resolve();
                } else {
                    previousText = currentText;
                }

                elapsed += interval;
                if (elapsed >= timeout) {
                    clearInterval(check);
                    console.log('Article stabilization timed out. Proceeding anyway.');
                    resolve();
                }
            }, interval);
        });
    }

    // Step 4: Trigger the next steps
    async function triggerNextSteps() {
        console.log('Step 4: Triggering next steps.');

        const promptDiv = await waitForElement('#prompt-textarea');
        promptDiv.innerHTML = '<p>Go ahead and continue with your next steps</p>';
        promptDiv.dispatchEvent(new Event('input', { bubbles: true }));

        const sendButton = await waitForElement('button[data-testid="send-button"]');
        if (!sendButton.disabled) {
            sendButton.click();
            console.log('Next steps sent successfully.');
        } else {
            console.log('Send button is disabled. Unable to send next steps.');
        }
    }

    // Start the script
    monitorForArticles();
})();