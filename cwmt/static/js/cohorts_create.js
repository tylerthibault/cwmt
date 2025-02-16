document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.getElementById('next-btn');
    const backBtn = document.getElementById('back-btn');
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const templateSelect = document.getElementById('template_id');

    nextBtn.addEventListener('click', function() {
        const templateId = templateSelect.value;
        if (!templateId) return;
        fetch(`/dashboard/cohorts/template/${templateId}`)
            .then(response => response.json())
            .then(data => {
                // Populate the fields with data from the template
                if(data.name) document.getElementById('name').value = data.name;
                if(data.max_capacity) document.getElementById('max_capacity').value = data.max_capacity;
                if(data.description) document.getElementById('description').value = data.description;
                if(data.start_date) document.getElementById('start_date').value = data.start_date;
                if(data.number_of_days) document.getElementById('number_of_days').value = data.number_of_days;
                // Populate fields with default data from the template
                if(data.default_max_capacity)
                    document.getElementById('max_capacity').value = data.default_max_capacity;
                if(data.default_number_of_days)
                    document.getElementById('number_of_days').value = data.default_number_of_days;
                // Transition to step 2
                step1.style.display = 'none';
                step2.style.display = 'block';
            })
            .catch(err => console.error('Error fetching template defaults', err));
    });

    backBtn.addEventListener('click', function() {
        // Go back to step 1
        step2.style.display = 'none';
        step1.style.display = 'block';
    });
});
