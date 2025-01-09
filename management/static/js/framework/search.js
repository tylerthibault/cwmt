export class ComponentSearch {
    /**
     * @param {Object} options - Configuration options
     * @param {string} [options.inputId='componentSearch'] - ID of search input element
     * @param {string} [options.containerId] - ID of container element
     */
    constructor(options = {}) {
        this.searchInput = document.getElementById(options.inputId || 'componentSearch');
        if (!this.searchInput) {
            console.error('Search input element not found');
            return;
        }

        this.container = options.containerId ? 
            document.getElementById(options.containerId) : 
            document.body;
            
        if (!this.container) {
            console.error('Container element not found');
            return;
        }

        this.searchableBoxes = this.container.querySelectorAll('.searchable-box');
        this.init();
    }

    init() {
        this.searchInput.addEventListener('input', () => this.filterComponents());
    }

    filterComponents() {
        const searchTerm = this.searchInput.value.toLowerCase();
        
        this.searchableBoxes.forEach(box => {
            const searchableElement = box.querySelector('.searchable-text');
            if (!searchableElement) return;

            const searchText = searchableElement.textContent;
            const isVisible = searchText.toLowerCase().includes(searchTerm);
            box.style.display = isVisible ? 'block' : 'none';
        });
    }
}