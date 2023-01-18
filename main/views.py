from django.shortcuts import render
from submissions.models import Submission


def main_page_view(request):
    submissions = Submission.objects.all()
    context = {'submissions': submissions}
    return render(request, 'public/mainpage.html', context)
