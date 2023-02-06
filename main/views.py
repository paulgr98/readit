from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from submissions.models import Submission
from comments.models import Comment
from users.models import ReaditUser

def main_page_view(request):
    readit_user = None
    try:
        readit_user = ReaditUser.objects.get(id=request.user.id)
    except:
        pass

    submissions = Submission.objects.all()
    context = {
        'submissions': submissions,
        'readit_user': readit_user 
    }

    return render(request, 'public/mainpage.html', context)


def upvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        submission.upvotes += 1
        submission.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def upvote_unclicked(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        submission.upvotes -= 1
        submission.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


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
