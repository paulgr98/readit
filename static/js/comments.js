
function postComment(submission_id) {
        const errorMsg = $('#create-comment-error-message');
        const content = $('#comment-input-content').val();
        if(content.length === 0) {
            errorMsg.attr('hidden', false);
            errorMsg.text('Comment content cannot be empty.');
            return;
        }

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: `/create-comment/${submission_id}`,
            type: 'POST',
            headers: { "X-CSRFToken": csrftoken },
            data: { content: content },
            success: function() {   
                errorMsg.attr('hidden', true);
                errorMsg.text('');
                location.reload();
            },
            error: function(xhr) {
                errorMsg.attr('hidden', false);
                errorMsg.text(xhr.responseText);
            }
        });
}