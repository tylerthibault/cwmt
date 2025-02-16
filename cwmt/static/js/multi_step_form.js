document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.multi-step-form').forEach(form => {
        const nextBtn = form.querySelector('[data-step="next"]');
        const backBtn = form.querySelector('[data-step="back"]');
        const step1 = form.querySelector('.step-1');
        const step2 = form.querySelector('.step-2');
        const fetchEndpoint = form.dataset.fetchEndpoint; // e.g., "/dashboard/cohorts/template"
        const fetchTrigger = form.querySelector('[data-fetch-trigger]');

        if(nextBtn) {
            nextBtn.addEventListener('click', function() {
                const param = fetchTrigger.value;
                if (!param) return;
                fetch(`${fetchEndpoint}/${param}`)
                    .then(response => response.json())
                    .then(data => {
                        // Populate fields based on mappings
                        form.querySelectorAll('[data-fetch-field]').forEach(elem => {
                            const key = elem.dataset.fetchField;
                            if(data[key] !== undefined) {
                                elem.value = data[key];
                            }
                        });
                        step1.style.display = 'none';
                        step2.style.display = 'block';
                    })
                    .catch(err => console.error('Error fetching defaults:', err));
            });
        }
        if(backBtn) {
            backBtn.addEventListener('click', function() {
                step2.style.display = 'none';
                step1.style.display = 'block';
            });
        }
    });
});
