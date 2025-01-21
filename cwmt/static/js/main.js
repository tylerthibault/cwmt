// modals
document.addEventListener('DOMContentLoaded', function () {
    const modalButtons = document.querySelectorAll('.modal-btn');

    modalButtons.forEach(function (btn) {
        btn.onclick = function () {
            const modal = btn.getAttribute('data-target').replace('#', '');

            const id = btn.getAttribute('data-id');

            document.querySelector(`.${modal}-id`).value = id;
            
        };
    });
});

console.log('main.js loaded');

