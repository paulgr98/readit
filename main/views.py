from django.http import JsonResponse
from django.shortcuts import render
from submissions.models import Submission


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


def downvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        submission.downvotes += 1
        submission.save()
        return JsonResponse({'status': 'success'})
