// HTML Example: <span class="editable" data-id="{{ team.id }}" data-route="{{ url_for('teams.update') }}">{{ team.name }}</span>

document.addEventListener('DOMContentLoaded', function () {
    // window.initEditableFields = function(updateUrl, selector = '.editable') {
    document.querySelectorAll('.editable').forEach(function (span) {
        span.addEventListener('click', function () {
            if (span.querySelector('input')) return;
            const originalText = span.innerText;
            const input = document.createElement('input');
            input.type = 'text';
            input.value = originalText;
            input.style.width = "100%";
            span.innerHTML = '';
            span.appendChild(input);
            input.focus();
            input.addEventListener('blur', function () {
                const newValue = input.value;
                span.innerText = newValue;
                const route = span.getAttribute('data-route');
                const id = span.getAttribute('data-id');
                const column_name = span.getAttribute('data-column-name');
                const formData = new FormData();
                formData.append('id', id);
                formData.append(column_name, newValue);
                fetch(route, {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => window.location.reload())
                    .catch(error => window.location.reload());
            });
        });
    });
    // }
});
