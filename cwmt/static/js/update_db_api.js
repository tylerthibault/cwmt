// HTML Example: <span class="editable" data-id="{{ team.id }}" data-column-name="id" data-route="{{ url_for('teams.update') }}">{{ team.name }}</span>

// @locations_bp.post('/api/dashboard/locations/update')
// def update():
//     id = request.form.get('id')
//     location = Location.get(id=id)
//     if not location:
//         core.logger.log(f'Location with ID {id} not found.', with_flash=True, status='error')
//         return jsonify({'status': 'error'})
    
//     location.update(request.form)
//     core.logger.log(f'Location {location.name} updated.', with_flash=True, flash_category='success')
//     return jsonify({'status': 'success'})

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
