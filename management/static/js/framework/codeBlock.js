export class CodeBlock {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('pre').forEach(block => {
            const button = document.createElement('button');
            button.className = 'code-copy-btn';
            button.innerHTML = 'Copy';
            
            button.addEventListener('click', () => this.copyCode(block, button));
            block.appendChild(button);
        });
    }

    async copyCode(block, button) {
        const code = block.querySelector('code').textContent;
        await navigator.clipboard.writeText(code);
        
        button.innerHTML = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.innerHTML = 'Copy';
            button.classList.remove('copied');
        }, 2000);
    }
}