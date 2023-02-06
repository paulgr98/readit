from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from submissions.models import Submission, Upvote
from comments.models import Comment
from users.models import ReaditUser


def main_page_view(request):
    readit_user = None
    has_upvoted = False
    try:
        readit_user = ReaditUser.objects.get(id=request.user.id)
        has_upvoted = Upvote.objects.filter(user=request.user, upvoted=True).exists()
    except:
        pass

    submissions = Submission.objects.all()
    context = {
        'submissions': submissions,
        'readit_user': readit_user,
        'has_upvoted': has_upvoted
    }

    return render(request, 'public/mainpage.html', context)


def upvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        upvote_obj, created = Upvote.objects.get_or_create(user=request.user, submission=submission)
        if not created:
            if upvote_obj.upvoted:
                submission.upvotes -= 1
                upvote_obj.upvoted = False
            else:
                submission.upvotes += 1
                upvote_obj.upvoted = True
        else:
            submission.upvotes += 1
            upvote_obj.upvoted = True
        upvote_obj.save()
        submission.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def upvote_unclicked(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        upvote_obj = Upvote.objects.filter(user=request.user, submission=submission).first()
        if upvote_obj:
            submission.upvotes -= 1
            submission.save()
            upvote_obj.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Upvote does not exist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def downvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        submission.downvotes += 1
        submission.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def comments_view(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    comments = Comment.objects.filter(submission=submission)
    has_user_commented = False
    if request.user.is_authenticated:
        has_user_commented = any([comment.user.id == request.user.id for comment in comments])

    context = {'submission': submission, 'comments': comments, 'has_user_commented': has_user_commented}
    return render(request, 'public/comments.html', context)
