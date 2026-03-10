// Photo Gear Guide - Main JavaScript

(function() {
    'use strict';

    // ページ読み込み時の初期化
    document.addEventListener('DOMContentLoaded', function() {
        initSmoothScroll();
        initExternalLinks();
        console.log('Photo Gear Guide loaded');
    });

    // スムーズスクロール
    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // 外部リンクに rel="noopener noreferrer" を自動付与
    function initExternalLinks() {
        const links = document.querySelectorAll('a[href^="http"]');
        links.forEach(link => {
            if (!link.hostname.includes(window.location.hostname)) {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            }
        });
    }

})();
