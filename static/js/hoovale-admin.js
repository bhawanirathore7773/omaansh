/* HOOVALE Admin — small-screen navigation helpers */
(function () {
    "use strict";

    function isMobile() {
        return window.matchMedia("(max-width: 1023px)").matches;
    }

    function closeNativeSidebar() {
        if (!isMobile()) return;

        // Let Unfold handle the actual drawer state. We only trigger its
        // existing close/toggle control when it is available.
        var selectors = [
            'button[aria-label*="close sidebar" i]',
            'button[title*="close sidebar" i]',
            'button[data-sidebar-close]',
            'button[aria-label*="sidebar" i][aria-expanded="true"]',
            'button[title*="sidebar" i][aria-expanded="true"]',
            'button[aria-expanded="true"][data-sidebar-toggle]'
        ];

        for (var i = 0; i < selectors.length; i++) {
            var buttons = document.querySelectorAll(selectors[i]);
            for (var j = 0; j < buttons.length; j++) {
                var button = buttons[j];
                if (button.offsetParent !== null) {
                    button.click();
                    return;
                }
            }
        }
    }

    function bindNavigation() {
        document.querySelectorAll("aside a, nav[aria-label] a").forEach(function (link) {
            if (link.dataset.hoovaleNavBound === "1") return;
            link.dataset.hoovaleNavBound = "1";

            link.addEventListener("click", function () {
                // Navigation remains a normal anchor navigation; this simply
                // lets the drawer close immediately on touch devices.
                if (isMobile()) {
                    window.setTimeout(closeNativeSidebar, 80);
                }
            });
        });
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && isMobile()) {
            closeNativeSidebar();
        }
    });

    document.addEventListener("DOMContentLoaded", bindNavigation);

    var observer = new MutationObserver(bindNavigation);
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
})();
