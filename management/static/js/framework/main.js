import { Modal } from './modal.js';
import { TabManager } from './tabs.js';
import { ComponentSearch } from './search.js';

const modalInstances = new Map();

document.addEventListener('DOMContentLoaded', () => {
    // Initialize modals
    document.querySelectorAll('.modal-wrapper').forEach((modal) => {
        const modalId = modal.id;
        modalInstances.set(modalId, new Modal(modalId));
        modal.addEventListener('modal:open', () => {
            console.log(`Modal ${modalId} opened`);
        });
    });

    // Initialize modal buttons
    document.querySelectorAll('.openModalBtn').forEach((button) => {
        button.addEventListener('click', () => {
            const targetModalId = button.getAttribute('data-modal-target');
            const modalInstance = modalInstances.get(targetModalId);
            if (modalInstance) {
                modalInstance.open();
            }
        });
    });

    // Initialize tabs
    const tabContainer = document.querySelector('.tab-container');
    if (tabContainer) {
        new TabManager(tabContainer);
    }

    // Initialize all search components
    document.querySelectorAll('.componentSearch').forEach(searchInput => {
        const containerId = searchInput.getAttribute('data-search-container');
        console.log('Container ID:', containerId);
        if (containerId) {
            new ComponentSearch({
                inputId: searchInput.id,
                containerId: containerId
            });
        }
    });
});