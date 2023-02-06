import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from submissions.models import Submission
from .forms import SubmissionForm
from users.models import ReaditUser


def create_or_edit_submission(request, submission_id):
    if not request.user.is_authenticated:
        return render(request, '..\\templates\public\\forbidden.html')

    if submission_id != 0:
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.author.id != request.user.id:
                return render(request, '..\\templates\public\\forbidden.html')
        except:
            return render(request, '..\\templates\public\\not-found.html')

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            author = ReaditUser.objects.get(id=request.user.id)
            if submission_id == 0:
                submission = Submission()
            submission.title = form.cleaned_data['title']
            submission.text = form.cleaned_data['text']
            submission.image_url = form.cleaned_data['image_url']
            submission.author = author
            submission.subreadit = form.cleaned_data['subreadit']
            submission.save()

            return redirect('/')
    else:
        if submission_id != 0:
            form = SubmissionForm(initial={
                'title': submission.title,
                'text': submission.text,
                'image_url': submission.image_url,
                'subreadit': submission.subreadit
            })
        else:
            form = SubmissionForm()

    return render(request, '..\\templates\public\\create-or-edit-submission.html',
                  {'form': form, 'action_name': 'Create' if submission_id == 0 else 'Edit'})


def delete_submission(request):
    try:
        submission = Submission.objects.get(id=request.POST['submission_id'])
        print('user id', request.user.id)
        if submission.author.id != request.user.id:
            return render(request, '..\\templates\public\\forbidden.html')
        submission.delete()
    except:
        return render(request, '..\\templates\public\\not-found.html')

    return HttpResponse(status=200)
