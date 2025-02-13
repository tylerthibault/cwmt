document.addEventListener('DOMContentLoaded', () => {
    // Open modal on button click
    document.querySelectorAll('[data-modal-target]').forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-modal-target');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'block';
            }
        });
    });

    // Close modal on close button click
    document.querySelectorAll('.modal .close-button').forEach(span => {
        span.addEventListener('click', () => {
            const modal = span.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Close modal on clicking outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
});
