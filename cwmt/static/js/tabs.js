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
        });
    });
});



console.log('tabs.js loaded');