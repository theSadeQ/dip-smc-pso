/**
 * ============================================================================
 * DIP-SMC-PSO Documentation - Back to Top Button
 * ============================================================================
 * Provides smooth scroll-to-top functionality for improved navigation on
 * long documentation pages.
 */

(function() {
    'use strict';

    /**
     * Initialize Back to Top button functionality
     */
    function initBackToTop() {
        // Create back to top button element
        const backToTop = document.createElement('div');
        backToTop.className = 'back-to-top';
        backToTop.innerHTML = '↑';
        backToTop.setAttribute('title', 'Back to top');
        backToTop.setAttribute('role', 'button');
        backToTop.setAttribute('aria-label', 'Scroll to top');
        backToTop.setAttribute('tabindex', '0');

        // Append to body
        document.body.appendChild(backToTop);

        // Show/hide button based on scroll position
        let scrollTimeout;
        function handleScroll() {
            // Debounce scroll events for better performance
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;

                if (scrollPosition > 300) {
                    backToTop.classList.add('show');
                } else {
                    backToTop.classList.remove('show');
                }
            }, 50);
        }

        // Smooth scroll to top functionality
        function scrollToTop(event) {
            event.preventDefault();

            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });

            // Focus management for accessibility
            setTimeout(() => {
                // Focus on main content or first heading after scroll
                const mainContent = document.querySelector('main h1, article h1, .document h1');
                if (mainContent) {
                    mainContent.setAttribute('tabindex', '-1');
                    mainContent.focus();
                    mainContent.removeAttribute('tabindex');
                }
            }, 500);
        }

        // Event listeners
        window.addEventListener('scroll', handleScroll, { passive: true });
        backToTop.addEventListener('click', scrollToTop);

        // Keyboard accessibility (Enter or Space key)
        backToTop.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                scrollToTop(event);
            }
        });

        // Initial check
        handleScroll();
    }

    /**
     * Make table of contents sticky on long pages
     */
    function makeTOCSticky() {
        const toc = document.querySelector('.toc-tree, .contents.local, nav.contents');

        if (toc && !toc.classList.contains('toc-scroll')) {
            // Only apply if page is long enough
            const pageHeight = document.documentElement.scrollHeight;
            const viewportHeight = window.innerHeight;

            if (pageHeight > viewportHeight * 2) {
                toc.classList.add('toc-scroll');
            }
        }
    }

    /**
     * Enhance download links with better styling
     */
    function enhanceDownloadLinks() {
        const downloadLinks = document.querySelectorAll('a.download, a[download]');

        downloadLinks.forEach(link => {
            if (!link.classList.contains('download-link')) {
                link.classList.add('download-link');
            }
        });
    }

    /**
     * Add smooth scroll behavior to all internal links
     */
    function addSmoothScrollToInternalLinks() {
        const internalLinks = document.querySelectorAll('a[href^="#"]');

        internalLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    event.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // Update URL without jumping
                    if (history.pushState) {
                        history.pushState(null, null, '#' + targetId);
                    }
                }
            });
        });
    }

    /**
     * Initialize all enhancements when DOM is ready
     */
    function init() {
        initBackToTop();
        makeTOCSticky();
        enhanceDownloadLinks();
        addSmoothScrollToInternalLinks();

        console.log('DIP-SMC-PSO Documentation enhancements loaded');
    }

    // Run initialization when DOM is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM already loaded
        init();
    }

})();
