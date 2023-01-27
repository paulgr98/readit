from django.http import JsonResponse
from django.shortcuts import render
from submissions.models import Submission
from comments.models import Comment


def main_page_view(request):
    submissions = Submission.objects.all()
    context = {'submissions': submissions}
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
    context = {'submission': submission, 'comments': comments}
    return render(request, 'public/comments.html', context)
