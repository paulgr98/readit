$(document).ready(function () {
    $('#sign-in-btn').click(function () {
        const signInForm = $('#sign-in-form');
        const signInError = $('#sign-in-error-message');
        $.ajax({
            url: '/sign-in',
            type: 'POST',
            data: signInForm.serialize(),
            success: function() {
                window.location.href = '/';
                signInForm[0].reset();
                signInError.attr('hidden', true);
                signInError.text('');
            },
            error: function() {
                signInError.attr('hidden', false);
                signInError.text('Username or password is invalid.');
            }
        })
    });
});

$(document).ready(function () {
    $('.sign-out-btn').click(function () {
        const choice = confirm('Are you sure you want to sign out?');
        if(choice) {
            $.ajax({
                url: '/sign-out',
                type: 'POST',
                data: $('#sign-out-form').serialize(),
                success: function () {
                    window.location.href = '/';
                },
                error: function() {
                    alert('Error while trying to sign out.');
                }
            })
        }
    });
});
