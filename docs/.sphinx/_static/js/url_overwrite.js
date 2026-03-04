// overwrite links.js

// Replace oldDomain with newDomain
const oldDomain = 'canonical-ubuntu-server.readthedocs-hosted.com';
const newDomain = 'ubuntu.com/server/docs';

// // Logging for debugging purposes
// console.stdlog = console.log.bind(console);
// console.logs = [];

// console.log = function() {
//     // 1. Store the arguments in the logs array
//     console.logs.push(Array.from(arguments));

//     // 2. Call the original console.log to still output to the browser console
//     console.stdlog.apply(console, arguments);
// };

// Set up a mutation observer to monitor changes in the DOM
// RTD flyout is created dynamically, so we need to wait for it to appear
const targetNode = document.body;
const config = { childList: true, subtree: true };

// Callback function to execute when mutation is observed
function waitForElement(element, callback){
    var foo = setInterval(function(){
        // console.log(`Waiting for element: ${element}...`)
        if(document.querySelector(element)){
            clearInterval(foo);
            // console.log(`Element found: ${element}.`)
            callback();
        }
    }, 100);
}

// Start observing the target node (rtd-flyout)
// execute the overwrite when the element is loaded 
waitForElement("readthedocs-flyout", function(){
    // console.log(`Triggering URL rewrite`)
    const rtdFlyout = document.querySelector('readthedocs-flyout');
    rtdFlyout.addEventListener('click', function(e) {
        // Access the shadow DOM of the 'readthedocs-flyout' element
        const shadowRoot = rtdFlyout.shadowRoot;
        const anchors = shadowRoot.querySelectorAll('a');
        anchors.forEach(anchor => {
            // console.log(`Checking URL for replacement: ${anchor.href}`);
            anchor.href = anchor.href.replace(new RegExp(oldDomain, 'g'), newDomain);
            // console.log(`URL now: ${anchor.href}`);
        });
    });
});