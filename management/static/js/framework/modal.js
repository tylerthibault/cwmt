export class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = this.modal.querySelector('.close-modal');
        this.isOpen = false;
        this.init();
    }

    init() {
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    open() {
        console.log('Opening modal'); // Debug
        this.modal.classList.remove('hidden');
        this.modal.classList.add('flex');
        this.isOpen = true;
        this.modal.dispatchEvent(new Event('modal:open'));
    }
    
    close() {
        console.log('Closing modal'); // Debug
        // this.modal.style.display = 'none';
        // this.modal.style.visibility = 'hidden';
        // document.body.style.overflow = 'auto';
        this.modal.classList.remove('flex');
        this.modal.classList.add('hidden');
        
        this.isOpen = false;
        this.modal.dispatchEvent(new Event('modal:close'));
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    setContent(content) {
        const modalContent = this.modal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.innerHTML = content;
        }
    }
}