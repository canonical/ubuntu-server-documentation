/**
 * Hoverxref Dark Mode Support
 * 
 * This script ensures that hoverxref tooltips (powered by Tippy.js) 
 * adapt to the current theme (light/dark mode).
 * 
 * Tippy.js appends tooltip elements directly to the body, outside the 
 * themed content area, so we need to dynamically update their styling
 * based on the current theme.
 */

(function() {
    'use strict';

    /**
     * Get the current theme from the body's data-theme attribute
     * @returns {string} 'light', 'dark', or 'auto'
     */
    function getCurrentTheme() {
        return document.body.getAttribute('data-theme') || 'auto';
    }

    /**
     * Determine if dark mode should be active
     * @returns {boolean}
     */
    function isDarkMode() {
        const theme = getCurrentTheme();
        if (theme === 'dark') {
            return true;
        } else if (theme === 'light') {
            return false;
        } else {
            // Theme is 'auto', check system preference
            return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
    }

    /**
     * Update all visible tooltips to match the current theme
     */
    function updateTooltipThemes() {
        const tooltips = document.querySelectorAll('.tippy-box');
        const darkMode = isDarkMode();
        
        tooltips.forEach(function(tooltip) {
            if (darkMode) {
                tooltip.classList.add('dark-mode');
            } else {
                tooltip.classList.remove('dark-mode');
            }
        });
    }

    /**
     * Set up a MutationObserver to watch for new tooltips being added to the DOM
     */
    function observeTooltips() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    // Check if the added node is a tooltip or contains tooltips
                    if (node.nodeType === 1) { // Element node
                        if (node.classList && node.classList.contains('tippy-box')) {
                            // A tooltip was added
                            if (isDarkMode()) {
                                node.classList.add('dark-mode');
                            }
                        } else if (node.querySelectorAll) {
                            // Check for tooltips within the added node
                            const tooltips = node.querySelectorAll('.tippy-box');
                            if (tooltips.length > 0 && isDarkMode()) {
                                tooltips.forEach(function(tooltip) {
                                    tooltip.classList.add('dark-mode');
                                });
                            }
                        }
                    }
                });
            });
        });

        // Observe the body for tooltip additions
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Watch for theme changes on the body element
     */
    function observeThemeChanges() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                    updateTooltipThemes();
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['data-theme']
        });
    }

    /**
     * Watch for system color scheme preference changes
     */
    function observeSystemThemeChanges() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            // Modern browsers
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', function() {
                    // Only update if theme is set to 'auto'
                    if (getCurrentTheme() === 'auto') {
                        updateTooltipThemes();
                    }
                });
            } else if (mediaQuery.addListener) {
                // Fallback for older browsers
                mediaQuery.addListener(function() {
                    if (getCurrentTheme() === 'auto') {
                        updateTooltipThemes();
                    }
                });
            }
        }
    }

    /**
     * Initialize the dark mode support
     */
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                observeTooltips();
                observeThemeChanges();
                observeSystemThemeChanges();
                updateTooltipThemes();
            });
        } else {
            observeTooltips();
            observeThemeChanges();
            observeSystemThemeChanges();
            updateTooltipThemes();
        }
    }

    // Start the script
    init();
})();
