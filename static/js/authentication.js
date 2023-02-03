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
                signUpForm[0].reset();
                signUpError.attr('hidden', true);
                signUpError.text('');
                confirm('Readit account created successfully. Now you can sign in.');
                window.location.href = '/';
            },
            error: function(xhr) {
                signUpError.attr('hidden', false);
                signUpError.text(xhr.responseText);
            }
        })
    });
});
