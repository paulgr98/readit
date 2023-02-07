from django.shortcuts import render
from .models import Subreadit
from submissions.models import Submission


# Create your views here.
def subreadit_view(request, name):
    try:
        subreadit = Subreadit.objects.get(name=name)
        submissions = Submission.objects.filter(subreadit=subreadit)
        # sort sumbissions by upvotes
        submissions = sorted(submissions, key=lambda x: x.upvotes, reverse=True)
        context = {'subreadit': subreadit, 'submissions': submissions}
        return render(request, 'public/subreadit.html', context)
    except:
        return render(request, 'public/not-found.html')
