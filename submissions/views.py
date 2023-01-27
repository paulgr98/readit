from django.shortcuts import render, redirect
from submissions.models import Submission
from .forms import SubmissionForm
from users.models import ReaditUser

def create_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            # hardcoded until log in will be implemented
            author = ReaditUser.objects.get(id=100)
            #
                        
            submission = Submission()
            submission.title = form.cleaned_data['title']
            submission.text = form.cleaned_data['text']
            submission.image_url = form.cleaned_data['image_url']
            submission.author = author
            submission.subreadit = form.cleaned_data['subreadit']
            submission.save()

            return redirect('/')
    else:
        form = SubmissionForm()

    return render(request, 'create-submission.html', {'form': form})