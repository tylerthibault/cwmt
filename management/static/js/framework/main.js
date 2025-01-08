import { Modal } from './modal.js';

// Cache modal instances
const modalInstances = new Map();

// Initialize all modals once
document.querySelectorAll('.modal-wrapper').forEach((modal) => {
    const modalId = modal.id;
    // Create and store modal instance
    modalInstances.set(modalId, new Modal(modalId));
    
    // Add event listener
    modal.addEventListener('modal:open', () => {
        console.log(`Modal ${modalId} opened`);
    });
});

// Handle open button clicks
document.querySelectorAll('.openModalBtn').forEach((button) => {
    button.addEventListener('click', () => {
        const targetModalId = button.getAttribute('data-modal-target');
        const modalInstance = modalInstances.get(targetModalId);
        if (modalInstance) {
            modalInstance.open();
        }
    });
});