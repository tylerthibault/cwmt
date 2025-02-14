document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tabbar .tab');
    const panels = document.querySelectorAll('.tab-panel');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Hide all panels
            panels.forEach(p => p.classList.remove('active'));
            // Activate selected tab and its panel
            this.classList.add('active');
            document.getElementById(this.getAttribute('data-tab')).classList.add('active');
            // Update URL parameter for the selected tab
            let url = new URL(window.location);
            url.searchParams.set('tab', this.getAttribute('data-tab'));
            history.pushState({}, '', url);
        });
    });
});

console.log('tabs.js loaded');