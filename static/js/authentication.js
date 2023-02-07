$(document).ready(function () {
    $('#sign-in-btn').click(function () {
        const signInForm = $('#sign-in-form');
        const signInError = $('#sign-in-error-message');
        $.ajax({
            url: '/sign-in',
            type: 'POST',
            data: signInForm.serialize(),
            success: function() {
                signInError.attr('hidden', true);
                signInError.text('');
                signInForm[0].reset();
                location.reload();
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
                    location.reload();
                },
                error: function() {
                    alert('Error while trying to sign out.');
                }
            })
        }
    });
});

$(document).ready(function () {
    $('#sign-up-btn').click(function () {
        const signUpForm = $('#sign-up-form');
        const signUpError = $('#sign-up-error-message');
        const password = $('#sign-up-password').val();
        const confirmPassword = $('#sign-up-confirm-password').val();
        console.log(password);
        console.log(confirmPassword);
        if(password !== confirmPassword) {
            signUpError.attr('hidden', false);
            signUpError.text('Passwords do not match.');
            return;
        }

        $.ajax({
            url: '/sign-up',
            type: 'POST',
            data: signUpForm.serialize(),
            success: function() {
                signUpError.attr('hidden', true);
                signUpError.text('');
                confirm('Readit account created successfully. Now you can sign in.');
                signUpForm[0].reset();
                location.reload();
            },
            error: function(xhr) {
                signUpError.attr('hidden', false);
                signUpError.text(xhr.responseText);
            }
        })
    });
});

$(document).on('hide.bs.modal','#sign-up-modal', function () {
    $('#sign-up-form')[0].reset();
});

$(document).on('hide.bs.modal','#sign-in-modal', function () {
    $('#sign-in-form')[0].reset();
});