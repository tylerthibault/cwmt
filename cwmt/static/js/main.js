// modals
document.addEventListener('DOMContentLoaded', function () {
    const modalButtons = document.querySelectorAll('.modal-btn');

    modalButtons.forEach(function (btn) {
        btn.onclick = function () {
            const modalId = btn.getAttribute('data-target');
            const modal = document.querySelector(modalId);
            const dataAttributes = btn.dataset;

            // Iterate over all data attributes and set corresponding modal fields
            for (const key in dataAttributes) {
                if (dataAttributes.hasOwnProperty(key)) {
                    const input = modal.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = dataAttributes[key];
                    }
                }
            }
        };
    });
});

console.log('main.js loaded');

