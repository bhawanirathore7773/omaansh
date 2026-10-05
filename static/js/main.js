/**
 * Site interaction and enquiry scripts
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    // Native browser lazy-loading handles image scheduling.
    initializeSmoothScroll();
    initializeFormValidation();
    initializeFastNavigation();
    // Native browser navigation + CSS View Transitions handle page changes.
    // Avoid applying an opacity fade to <main>; it caused a white/blink flash on mobile.
    initializeProductEnquiry();
    initializeContactForm();
    initializeProductFilters();
    initializeProductPriceRange();
    initializeProductCardLinks();
    initializeCampaignCarousel();
});


/**
 * Paytm-style mobile campaign carousel.
 * Uses Bootstrap's horizontal slide transition, but handles the touch gesture
 * ourselves so a swipe never competes with Bootstrap's touch handler.
 */
function initializeCampaignCarousel() {
    const root = document.getElementById('hvHomeBanner');
    if (!root || root.dataset.hvCampaignBound === 'true') return;

    const viewport = root.querySelector('.hv-campaign-viewport');
    const track = root.querySelector('.hv-campaign-track');
    const originalSlides = Array.from(track ? track.children : []);
    const indicators = Array.from(root.querySelectorAll('.hv-banner-indicators button'));
    const prevButton = root.querySelector('.hv-campaign-prev');
    const nextButton = root.querySelector('.hv-campaign-next');

    if (!viewport || !track || originalSlides.length < 2) return;

    root.dataset.hvCampaignBound = 'true';

    // Build a true infinite strip: [last] [1] [2] ... [last] [first].
    const firstClone = originalSlides[0].cloneNode(true);
    const lastClone = originalSlides[originalSlides.length - 1].cloneNode(true);
    track.insertBefore(lastClone, originalSlides[0]);
    track.appendChild(firstClone);

    const slides = Array.from(track.children);
    const count = originalSlides.length;

    let index = 1;
    let width = 0;
    let slideWidth = 0;
    let gap = 8;
    let dragging = false;
    let horizontal = null;
    let startX = 0;
    let startY = 0;
    let moved = false;
    let dragBaseTranslate = 0;
    let autoplay = null;
    let correctionTimer = null;

    const realIndex = () => {
        if (index === 0) return count - 1;
        if (index === count + 1) return 0;
        return index - 1;
    };

    const updateIndicators = () => {
        const active = realIndex();
        indicators.forEach((button, i) => {
            const selected = i === active;
            button.classList.toggle('active', selected);
            button.setAttribute('aria-current', selected ? 'true' : 'false');
        });
    };

    const render = (translate, animated) => {
        track.classList.toggle('hv-animated', animated);
        track.style.transform = 'translate3d(' + translate + 'px,0,0)';
    };

    const measure = () => {
        width = viewport.getBoundingClientRect().width;
        if (!width) return;

        // Paytm-style "peek": each card is slightly narrower than the
        // viewport and has a small gap before the next card.
        gap = window.matchMedia('(min-width: 768px)').matches ? 10 : 8;
        // The banner itself fills the white carousel container edge-to-edge.
        // The small gap remains between adjacent slides while swiping.
        const horizontalPadding = 0;
        slideWidth = Math.max(1, width - horizontalPadding);

        track.style.width = ((slides.length * slideWidth) + ((slides.length - 1) * gap)) + 'px';
        slides.forEach(slide => {
            slide.style.width = slideWidth + 'px';
            slide.style.minWidth = slideWidth + 'px';
            slide.style.flex = '0 0 ' + slideWidth + 'px';
        });

        render(-(index * (slideWidth + gap)), false);
    };

    const normalize = () => {
        if (index === 0) {
            index = count;
            render(-(index * (slideWidth + gap)), false);
        } else if (index === count + 1) {
            index = 1;
            render(-(index * (slideWidth + gap)), false);
        }
        updateIndicators();
    };

    const goTo = (target, animated = true) => {
        index = target;
        updateIndicators();
        render(-(index * (slideWidth + gap)), animated);

        if (correctionTimer) clearTimeout(correctionTimer);
        if (animated) {
            correctionTimer = setTimeout(normalize, 420);
        } else {
            normalize();
        }
    };

    const stopAutoplay = () => {
        if (autoplay) {
            clearInterval(autoplay);
            autoplay = null;
        }
    };

    const restartAutoplay = () => {
        stopAutoplay();
        autoplay = setInterval(() => goTo(index + 1, true), 5200);
    };

    const next = () => {
        goTo(index + 1, true);
        restartAutoplay();
    };

    const prev = () => {
        goTo(index - 1, true);
        restartAutoplay();
    };

    indicators.forEach((button, i) => {
        button.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            goTo(i + 1, true);
            restartAutoplay();
        });
    });

    nextButton?.addEventListener('click', event => {
        event.preventDefault();
        next();
    });

    prevButton?.addEventListener('click', event => {
        event.preventDefault();
        prev();
    });

    viewport.addEventListener('pointerdown', event => {
        if (event.pointerType === 'mouse' && event.button !== 0) return;

        width = viewport.getBoundingClientRect().width;
        if (!width) return;

        dragging = true;
        horizontal = null;
        moved = false;
        startX = event.clientX;
        startY = event.clientY;

        stopAutoplay();

        // Do NOT move the carousel on pointer-down. A normal tap/click must
        // leave the banner visually locked in place. Capture the exact
        // on-screen transform so a real horizontal drag starts from where
        // the banner is currently rendered (including an in-progress autoplay).
        const currentTransform = window.getComputedStyle(track).transform;
        const matrixMatch = currentTransform && currentTransform !== 'none'
            ? currentTransform.match(/matrix\(([^)]+)\)/)
            : null;
        if (matrixMatch) {
            const values = matrixMatch[1].split(',').map(Number);
            dragBaseTranslate = Number.isFinite(values[4]) ? values[4] : -(index * (slideWidth + gap));
        } else {
            dragBaseTranslate = -(index * (slideWidth + gap));
        }

        viewport.classList.add('hv-is-dragging');

        try { viewport.setPointerCapture(event.pointerId); } catch (_) {}
    });

    viewport.addEventListener('pointermove', event => {
        if (!dragging) return;

        const dx = event.clientX - startX;
        const dy = event.clientY - startY;

        if (horizontal === null) {
            if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return;
            horizontal = Math.abs(dx) > Math.abs(dy);
        }

        if (!horizontal) return;

        moved = Math.abs(dx) > 6;

        // Do not preventDefault until the gesture is known to be horizontal.
        // This keeps normal page scrolling working.
        event.preventDefault();

        // Freeze the exact position only after the gesture is confirmed as
        // horizontal. This prevents the tiny jump seen when simply tapping
        // a banner.
        render(dragBaseTranslate + dx, false);
    });

    const release = event => {
        if (!dragging) return;

        const dx = event.clientX - startX;
        dragging = false;
        viewport.classList.remove('hv-is-dragging');

        if (!horizontal) {
            restartAutoplay();
            return;
        }

        const threshold = Math.max(45, slideWidth * 0.12);

        if (dx < -threshold) {
            next();
        } else if (dx > threshold) {
            prev();
        } else {
            render(-(index * (slideWidth + gap)), true);
            restartAutoplay();
        }

        horizontal = null;
    };

    viewport.addEventListener('pointerup', release);
    viewport.addEventListener('pointercancel', release);

    viewport.addEventListener('click', event => {
        if (!moved) return;
        event.preventDefault();
        event.stopPropagation();
        moved = false;
    }, true);

    window.addEventListener('resize', measure, { passive: true });

    // Never leave the whole page locked because of a stale mobile-menu class.
    if (!document.querySelector('.hv-mobile-drawer.is-open')) {
        document.body.classList.remove('hv-menu-open');
    }

    measure();
    updateIndicators();
    restartAutoplay();
}

/**
 * Smooth scroll behavior for anchor links
 */
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Simple form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Utility function to format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

/**
 * Add to cart functionality (for future use)
 */
function addToCart(productId) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const currentCount = parseInt(cartCount.textContent) || 0;
        cartCount.textContent = currentCount + 1;
    }
}

/**
 * Handle scroll position for sticky header
 */
window.addEventListener('scroll', function() {
    const header = document.querySelector('.sticky-header');
    if (window.scrollY > 50) {
        header?.classList.add('scrolled');
    } else {
        header?.classList.remove('scrolled');
    }
});

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Search products dynamically
 */
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function(e) {
        const query = this.value.trim();
        if (query.length > 2) {
            // Could trigger live search here
            console.log('Searching for:', query);
        }
    }, 300));
}

/**
 * Initialize tooltips (if using Bootstrap tooltips)
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Handle responsive navigation
 */
function setupResponsiveNav() {
    const toggler = document.getElementById('hvMenuToggle');
    const drawer = document.getElementById('nav');
    const overlay = document.getElementById('hvMenuOverlay');

    if (!toggler || !drawer) return;

    // Recover from a stale scroll lock after Android browser restore/BFCache.
    const clearStalePageLocks = () => {
        if (!drawer.classList.contains('is-open')) {
            document.documentElement.classList.remove('hv-menu-open');
            document.body.classList.remove('hv-menu-open');
        }
        if (!document.querySelector('.modal.show')) {
            document.documentElement.classList.remove('modal-open');
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('padding-right');
        }
    };

    clearStalePageLocks();

    // Keep Bootstrap's collapse class from fighting the custom drawer.
    drawer.classList.remove('show');

    const isMobile = () => window.matchMedia('(max-width: 991px)').matches;

    function setMenu(open) {
        if (!isMobile()) open = false;

        drawer.classList.toggle('is-open', open);
        drawer.classList.remove('show');
        overlay?.classList.toggle('is-visible', open);
        toggler.classList.toggle('is-open', open);
        toggler.setAttribute('aria-expanded', String(open));
        toggler.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
        overlay?.setAttribute('aria-hidden', String(!open));
        document.documentElement.classList.toggle('hv-menu-open', open);
        document.body.classList.toggle('hv-menu-open', open);
    }

    // Remove duplicate handlers if this initializer is ever called again.
    if (toggler.dataset.hvNavBound === 'true') return;
    toggler.dataset.hvNavBound = 'true';

    toggler.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        setMenu(!drawer.classList.contains('is-open'));
    });

    overlay?.addEventListener('click', () => setMenu(false));

    drawer.querySelectorAll('.nav-link, .nav-item .btn').forEach(link => {
        link.addEventListener('click', () => setMenu(false));
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') setMenu(false);
    });

    window.addEventListener('resize', () => {
        if (!isMobile()) setMenu(false);
    });

    setMenu(false);

    // Some Android browsers restore DOM/CSS state from BFCache.
    // Re-check when the page is restored or becomes visible again.
    window.addEventListener('pageshow', clearStalePageLocks);
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') clearStalePageLocks();
    });
}

// Initialize responsive navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupResponsiveNav);
} else {
    setupResponsiveNav();
}

/**
 * Fast same-site navigation
 *
 * Starts fetching important pages before the user taps them. This is
 * especially useful on mobile and on Render's free tier where a sleeping
 * instance can make the first request feel slow.
 */
function initializeFastNavigation() {
    const links = document.querySelectorAll(
        'a[href]:not([target="_blank"]):not([download]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])'
    );

    const prefetched = new Set();

    function isSameOriginPage(link) {
        try {
            const url = new URL(link.href, window.location.href);
            return (
                url.origin === window.location.origin &&
                url.pathname !== window.location.pathname &&
                !url.pathname.startsWith('/admin') &&
                !url.pathname.startsWith('/media/') &&
                !url.pathname.startsWith('/static/')
            );
        } catch (error) {
            return false;
        }
    }

    function prefetch(link) {
        if (!link || !isSameOriginPage(link)) return;

        const url = new URL(link.href, window.location.href);
        const key = url.href;

        if (prefetched.has(key)) return;
        prefetched.add(key);

        const prefetchLink = document.createElement('link');
        prefetchLink.rel = 'prefetch';
        prefetchLink.href = url.href;
        prefetchLink.as = 'document';
        prefetchLink.fetchPriority = 'low';
        document.head.appendChild(prefetchLink);
    }

    links.forEach(link => {
        link.addEventListener('mouseenter', () => prefetch(link), { passive: true });
        link.addEventListener('focus', () => prefetch(link), { passive: true });
        link.addEventListener('touchstart', () => prefetch(link), {
            passive: true,
            once: true
        });
    });

    // These are the most frequently used mobile destinations.
    ['/products/', '/categories/'].forEach(path => {
        const link = document.querySelector('a[href="' + path + '"]');
        if (link) prefetch(link);
    });
}

/**
 * Add a lightweight page transition so navigation feels intentional instead
 * of showing a sudden white flash while the next Django page loads.
 */
function initializePageTransitions() {
    // Kept as a compatibility hook for older cached pages.
    // Do not fade the current document before navigation: mobile browsers can
    // briefly paint the faded page/white background and create a visible blink.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    window.addEventListener('pageshow', function () {
        document.body.classList.remove('hv-page-leaving', 'hv-page-ready');
    }, { once: false });
}

/**
 * Price formatter for display
 */
function displayPrice(price) {
    if (!price) return 'Contact for Price';
    return '₹' + parseFloat(price).toLocaleString('en-IN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Press '/' to focus search
    if (e.key === '/' && searchInput) {
        e.preventDefault();
        searchInput.focus();
    }
    // Press 'Esc' to close modals
    if (e.key === 'Escape') {
        const modal = bootstrap.Modal.getOrCreateInstance(document.querySelector('.modal.show'));
        if (modal) modal.hide();
    }
});

/**
 * Performance monitoring
 */
if (window.performance && window.performance.timing) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const timing = window.performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            console.log('Page load time:', loadTime + 'ms');
        }, 0);
    });
}

/**
 * Service Worker registration for PWA (optional)
 */
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/static/js/service-worker.js');
    });
}

/**
 * Export functions for global use
 */
window.HOOVALE = {
    formatCurrency,
    addToCart,
    debounce,
    displayPrice
};

/* ============================================================
   PRODUCT FILTER DRAWER
   ============================================================ */
function initializeProductFilters() {
    const toggle = document.getElementById('productsFilterToggle');
    const drawer = document.getElementById('productsFilterDrawer');
    const backdrop = document.getElementById('productsFilterBackdrop');
    const close = document.getElementById('productsFilterClose');
    if (!toggle || !drawer || !backdrop) return;
    if (toggle.dataset.hvFilterBound === '1') return;

    toggle.dataset.hvFilterBound = '1';

    const setOpen = (open) => {
        document.body.classList.toggle('hv-filter-open', open);
        drawer.setAttribute('aria-hidden', String(!open));
        backdrop.setAttribute('aria-hidden', String(!open));
        toggle.setAttribute('aria-expanded', String(open));
    };

    toggle.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        setOpen(true);
    });

    backdrop.addEventListener('click', function(event) {
        event.preventDefault();
        setOpen(false);
    });

    close?.addEventListener('click', function(event) {
        event.preventDefault();
        setOpen(false);
    });

    drawer.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && document.body.classList.contains('hv-filter-open')) {
            setOpen(false);
        }
    });

    initializeProductPriceRange();
}


function initializeProductPriceRange() {
    const slider = document.getElementById('dualPriceSlider');
    const minRange = document.getElementById('minPriceRange');
    const maxRange = document.getElementById('maxPriceRange');
    const minInput = document.getElementById('minPriceInput');
    const maxInput = document.getElementById('maxPriceInput');
    const minOutput = document.getElementById('minPriceOutput');
    const maxOutput = document.getElementById('maxPriceOutput');
    const fill = document.getElementById('dualPriceFill');
    const form = document.getElementById('productsFilterForm');
    if (!slider || !minRange || !maxRange || !minInput || !maxInput) return;
    if (slider.dataset.bound === '1') return;
    slider.dataset.bound = '1';

    const min = Number(slider.dataset.min || minRange.min || 0);
    const max = Number(slider.dataset.max || maxRange.max || 0);
    const step = Number(minRange.step || 10);
    const clamp = v => Math.min(max, Math.max(min, Number(v) || min));

    const sync = source => {
        let lo = clamp(minRange.value);
        let hi = clamp(maxRange.value);
        if (lo > hi) {
            if (source === 'min') lo = hi;
            else hi = lo;
        }
        minRange.value = lo;
        maxRange.value = hi;
        minInput.value = lo === min ? '' : Math.round(lo);
        maxInput.value = hi === max ? '' : Math.round(hi);
        if (minOutput) minOutput.textContent = Math.round(lo).toLocaleString('en-IN');
        if (maxOutput) maxOutput.textContent = Math.round(hi).toLocaleString('en-IN');
        const span = Math.max(1, max - min);
        const left = ((lo - min) / span) * 100;
        const right = ((hi - min) / span) * 100;
        if (fill) {
            fill.style.left = left + '%';
            fill.style.right = (100 - right) + '%';
        }
    };

    minRange.addEventListener('input', () => sync('min'));
    maxRange.addEventListener('input', () => sync('max'));

    minInput.addEventListener('input', () => {
        if (minInput.value === '') { minRange.value = min; sync('min'); return; }
        minRange.value = clamp(Math.round(Number(minInput.value) / step) * step);
        sync('min');
    });
    maxInput.addEventListener('input', () => {
        if (maxInput.value === '') { maxRange.value = max; sync('max'); return; }
        maxRange.value = clamp(Math.round(Number(maxInput.value) / step) * step);
        sync('max');
    });

    document.querySelectorAll('[data-reset-group="price"]').forEach(btn => {
        btn.addEventListener('click', () => {
            minRange.value = min;
            maxRange.value = max;
            minInput.value = '';
            maxInput.value = '';
            sync();
            updateCount();
        });
    });

    document.querySelectorAll('[data-reset-group="category"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const radio = document.querySelector('input[name="category"][value=""]');
            if (radio) radio.checked = true;
            updateCount();
        });
    });
    document.querySelectorAll('[data-reset-group="badge"]').forEach(btn => {
        btn.addEventListener('click', () => { document.querySelectorAll('input[name="badge"]').forEach(i => i.checked = false); updateCount(); });
    });
    document.querySelectorAll('[data-reset-group="availability"]').forEach(btn => {
        btn.addEventListener('click', () => { document.querySelectorAll('input[name="availability"]').forEach(i => i.checked = false); updateCount(); });
    });

    const updateCount = () => {
        let count = 0;
        if (document.querySelector('input[name="category"]:checked')?.value) count++;
        const minBound = Number(slider?.dataset.min || minRange?.min || 0);
        const maxBound = Number(slider?.dataset.max || maxRange?.max || 0);
        const selectedMin = Number(minInput.value || minBound);
        const selectedMax = Number(maxInput.value || maxBound);
        if (selectedMin > minBound || selectedMax < maxBound) count++;
        if (document.querySelector('input[name="badge"]:checked')) count++;
        if (document.querySelector('input[name="availability"]:checked')) count++;

        const apply = document.getElementById('filterApplyButton');
        if (apply) apply.textContent = count ? `Apply Filters(${count})` : 'Apply Filters';
    };
    form?.addEventListener('input', updateCount);
    form?.addEventListener('change', updateCount);
    sync();
    updateCount();
}

/* Fallback delegated handler:
   keeps the mobile filter working even if the page is restored from cache
   or another script initializes after the normal DOM-ready pass. */
if (!window.__hoovaleFilterDelegationBound) {
    window.__hoovaleFilterDelegationBound = true;

    document.addEventListener('click', function(event) {
        const toggle = event.target.closest('#productsFilterToggle');
        if (toggle) {
            const drawer = document.getElementById('productsFilterDrawer');
            const backdrop = document.getElementById('productsFilterBackdrop');
            if (!drawer || !backdrop) return;

            event.preventDefault();
            event.stopPropagation();

            document.body.classList.add('hv-filter-open');
            drawer.setAttribute('aria-hidden', 'false');
            backdrop.setAttribute('aria-hidden', 'false');
            toggle.setAttribute('aria-expanded', 'true');
            return;
        }

        if (event.target.closest('#productsFilterClose, #productsFilterBackdrop')) {
            const drawer = document.getElementById('productsFilterDrawer');
            const backdrop = document.getElementById('productsFilterBackdrop');
            const toggle = document.getElementById('productsFilterToggle');

            document.body.classList.remove('hv-filter-open');
            drawer?.setAttribute('aria-hidden', 'true');
            backdrop?.setAttribute('aria-hidden', 'true');
            toggle?.setAttribute('aria-expanded', 'false');
        }
    }, true);
}

/* ============================================================
   PRODUCT CARD KEYBOARD NAVIGATION
   ============================================================ */
/* ============================================================
   PRODUCT ENQUIRY MODAL
   Opens the existing Bootstrap enquiry modal from product cards.
   ============================================================ */
function initializeProductEnquiry() {
    const modalEl = document.getElementById('enquiryModal');
    if (!modalEl) return;

    const buttons = document.querySelectorAll('.enquiry-btn');
    if (!buttons.length) return;

    buttons.forEach(button => {
        if (button.dataset.hvEnquiryBound === '1') return;
        button.dataset.hvEnquiryBound = '1';

        button.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();

            const productId = this.getAttribute('data-product-id') || '';
            const productName = this.getAttribute('data-product-name') || '';

            const productInput = document.getElementById('productId');
            const messageInput = document.getElementById('message');

            if (productInput) productInput.value = productId;
            if (messageInput && !messageInput.value.trim()) {
                messageInput.value = productName
                    ? 'I am interested in: ' + productName
                    : '';
            }

            const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            modal.show();
        });
    });

    // Bootstrap normally closes a modal from its backdrop, but keep an explicit
    // fallback so taps outside the dialog always close it on mobile Safari.
    if (modalEl.dataset.hvModalCloseBound !== '1') {
        modalEl.dataset.hvModalCloseBound = '1';
        modalEl.addEventListener('click', function (event) {
            if (event.target === modalEl) {
                bootstrap.Modal.getOrCreateInstance(modalEl).hide();
            }
        });
    }

    const form = document.getElementById('enquiryForm');
    if (form && form.dataset.hvEnquiryFormBound !== '1') {
        form.dataset.hvEnquiryFormBound = '1';

        form.addEventListener('submit', async function(event) {
            event.preventDefault();

            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.innerHTML : '';

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            }

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {'X-Requested-With': 'XMLHttpRequest'}
                });
                const data = await response.json();

                let message = document.getElementById('enquiryResponse');
                if (!message) {
                    message = document.createElement('div');
                    message.id = 'enquiryResponse';
                    form.prepend(message);
                }

                if (response.ok && data.success) {
                    message.innerHTML = '<div class="alert alert-success mb-3"><i class="fas fa-check-circle"></i> ' +
                        (data.message || 'Enquiry submitted successfully!') + '</div>';
                    form.reset();

                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(modalEl);
                        if (modal) modal.hide();
                        message.innerHTML = '';
                    }, 1800);
                } else {
                    message.innerHTML = '<div class="alert alert-danger mb-3"><i class="fas fa-exclamation-circle"></i> ' +
                        (data.error || 'Please check the details and try again.') + '</div>';
                }
            } catch (error) {
                let message = document.getElementById('enquiryResponse');
                if (!message) {
                    message = document.createElement('div');
                    message.id = 'enquiryResponse';
                    form.prepend(message);
                }
                message.innerHTML = '<div class="alert alert-danger mb-3"><i class="fas fa-exclamation-circle"></i> Network error. Please try again or WhatsApp us.</div>';
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            }
        });
    }

    // Keep the dynamically-created Bootstrap backdrop clickable as a fallback.
    if (!window.__hoovaleEnquiryBackdropBound) {
        window.__hoovaleEnquiryBackdropBound = true;
        document.addEventListener('click', function (event) {
            if (!event.target.classList?.contains('modal-backdrop')) return;

            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                bootstrap.Modal.getOrCreateInstance(openModal).hide();
            }
        }, true);
    }
}

function initializeProductCardLinks() {
    document.querySelectorAll('.product-card-link[role="link"]').forEach(card => {
        if (card.dataset.hvCardBound === '1') return;
        card.dataset.hvCardBound = '1';
        card.addEventListener('keydown', event => {
            if ((event.key === 'Enter' || event.key === ' ') && !event.target.closest('a,button')) {
                event.preventDefault();
                const url = card.dataset.productUrl;
                if (url) window.location.href = url;
            }
        });
    });
}

/* ============================================================
   CONTACT ENQUIRY FORM
   Works after instant page swaps as well as normal page loads.
   ============================================================ */
function initializeContactForm() {
    const form = document.getElementById('contactForm');
    if (!form || form.dataset.hvContactBound === '1') return;

    form.dataset.hvContactBound = '1';
    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const responseDiv = document.getElementById('formResponse');
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            });
            const data = await response.json();

            if (response.ok && data.success) {
                if (responseDiv) {
                    responseDiv.innerHTML =
                        '<div class="alert alert-success"> <i class="fas fa-check-circle"></i> ' +
                        (data.message || 'Enquiry sent successfully!') +
                        ' We will contact you soon.</div>';
                }
                form.reset();
            } else {
                if (responseDiv) {
                    responseDiv.innerHTML =
                        '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ' +
                        (data.error || 'Please check the details and try again.') +
                        '</div>';
                }
            }
        } catch (error) {
            if (responseDiv) {
                responseDiv.innerHTML =
                    '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ' +
                    'Network error. Please WhatsApp us directly.</div>';
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

