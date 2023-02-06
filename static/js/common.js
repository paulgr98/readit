$(document).ready(function () {
    $('#create-submission-card-input').click(function () {
        window.location.href = '/submit/0';
    });
});

$(document).ready(function () {
    $('.back-to-top-btn').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 'slow');  
    });
});