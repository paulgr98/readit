function deleteSubmission(id) {
    const choice = confirm('Are you sure you want to delete selected submission?');
    if(choice) {
        const form = $(`#delete-submission-form-${id}`);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: '/delete-submission',
            type: 'POST',
            headers: { "X-CSRFToken": csrftoken },
            data: form.serialize(),
            success: function () {
                window.location.href = '/';
            },
            error: function() {
                alert('Error while trying to delete submission.');
            }
        })
    }
}