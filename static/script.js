document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('upload-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('/upload/employee_list', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to upload files. ' + response.statusText);
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                const currentYear = new Date().getFullYear();
                a.href = url;
                a.download = `Secret_Santa_Result_${currentYear}.csv`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('An error occurred:', error.message);
            });
    });
});
