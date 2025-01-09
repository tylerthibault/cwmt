export class TabManager {
    constructor(container) {
        this.container = container;
        this.tabs = container.querySelectorAll('.tab-btn');
        this.panes = container.querySelectorAll('.tab-pane');
        this.state = {};
        this.init();
    }

    init() {
        // Tab button clicks
        this.tabs.forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab.dataset.tab));
        });

        // Next/Prev buttons
        this.container.querySelectorAll('.next-tab').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.next));
        });

        this.container.querySelectorAll('.prev-tab').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.prev));
        });
    }

    switchTab(tabId) {
        // Store current tab state
        this.saveState(this.getCurrentTab());
        
        // Update active states
        this.tabs.forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });
        
        this.panes.forEach(pane => {
            pane.classList.toggle('active', pane.id === tabId);
        });

        // Load new tab state
        this.loadState(tabId);
    }

    getCurrentTab() {
        return this.container.querySelector('.tab-pane.active').id;
    }

    saveState(tabId) {
        // Save form data for current tab
        const inputs = this.container.querySelectorAll(`#${tabId} input`);
        this.state[tabId] = Array.from(inputs).reduce((data, input) => {
            data[input.name] = input.value;
            return data;
        }, {});
    }

    loadState(tabId) {
        // Restore form data for tab
        if (this.state[tabId]) {
            Object.entries(this.state[tabId]).forEach(([name, value]) => {
                const input = this.container.querySelector(`#${tabId} input[name="${name}"]`);
                if (input) input.value = value;
            });
        }
    }
}