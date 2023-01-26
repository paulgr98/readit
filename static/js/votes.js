
function handle_upvote_click(args) {
    args.upvoteArrow.classList.add('upvote-clicked');
    fetch('/upvote/' + args.submissionId + '/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': args.csrftoken
        },
        body: JSON.stringify({
            'submission_id': args.submissionId
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {
            if (data.status === 'success') {
                let currentCount = parseInt(args.upvoteCountElement.textContent)
                args.upvoteCountElement.textContent = `${currentCount + 1}`
            }
        })
}

function handle_upvote_unclick(args) {
    fetch('/upvote_unclicked/' + args.submissionId + '/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': args.csrftoken
        },
        body: JSON.stringify({
            'submission_id': args.submissionId
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {
            if (data.status === 'success') {
                let currentCount = parseInt(args.upvoteCountElement.textContent)
                args.upvoteCountElement.textContent = `${currentCount - 1}`
            }
        })
}

function upvote(submissionId) {
    event.preventDefault();
    const csrftoken = document.querySelector("[name='csrfmiddlewaretoken']").value;

    const upvoteArrow = document.querySelector('.upvote-arrow-' + submissionId);
    const downvoteArrow = document.querySelector('.downvote-arrow-' + submissionId);
    const upvoteCountElement = document.querySelector('.upvote-counter-' + submissionId)

    if (upvoteArrow.classList.contains('upvote-clicked')) {
        upvoteArrow.classList.remove('upvote-clicked');
        handle_upvote_unclick({
                submissionId: submissionId,
                upvoteArrow: upvoteArrow,
                upvoteCountElement: upvoteCountElement,
                csrftoken: csrftoken
            })
    } else {
        handle_upvote_click({
                submissionId: submissionId,
                upvoteArrow: upvoteArrow,
                upvoteCountElement: upvoteCountElement,
                csrftoken: csrftoken
            })
        }

    if (downvoteArrow.classList.contains('downvote-clicked')) {
        downvoteArrow.classList.remove('downvote-clicked');
    }
}

function downvote(submissionId) {
    event.preventDefault();
    const csrftoken = document.querySelector("[name='csrfmiddlewaretoken']").value;

    const downvoteArrow = document.querySelector('.downvote-arrow-' + submissionId);
    const upvoteArrow = document.querySelector('.upvote-arrow-' + submissionId);
    const upvoteCountElement = document.querySelector('.upvote-counter-' + submissionId)

    if (downvoteArrow.classList.contains('downvote-clicked')) {
        downvoteArrow.classList.remove('downvote-clicked');
    } else {
        downvoteArrow.classList.add('downvote-clicked');
    }

    if (upvoteArrow.classList.contains('upvote-clicked')) {
        upvoteArrow.classList.remove('upvote-clicked');
        handle_upvote_unclick({
                submissionId: submissionId,
                upvoteArrow: upvoteArrow,
                upvoteCountElement: upvoteCountElement,
                csrftoken: csrftoken
            })
    }

    fetch('/downvote/' + submissionId + '/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'submission_id': submissionId
        })
    })
        .then(response => response.json())
}
