from django.shortcuts import render
from .models import ReaditUser
from submissions.models import Submission


# Create your views here.

def profile_view(request, username):
    user = ReaditUser.objects.get(user__username=username)
    submissions = Submission.objects.filter(author_id=user.user_id)
    # sort sumbissions by created_at date
    submissions = sorted(submissions, key=lambda x: x.created_at, reverse=True)
    context = {'user': user, 'submissions': submissions}
    return render(request, 'public/profile.html', context)
