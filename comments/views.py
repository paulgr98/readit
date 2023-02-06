from django.http import HttpResponse
from submissions.models import Submission
from users.models import ReaditUser
from .models import Comment

def create_comment(request, submission_id):
    submission = None
    try: 
        submission = Submission.objects.get(id=submission_id)
    except:
        return HttpResponse(status=400, content="Submission does not exist")
    
    readit_user = None
    try:
        readit_user = ReaditUser.objects.get(id=request.user.id)
    except:
        return HttpResponse(status=400, content="Readit user does not exist")
    
    if Comment.objects.filter(submission=submission, user=readit_user).exists():
        return HttpResponse(status=400, content="User comment for this submission already exists")
    
    comment = Comment(submission=submission, user=readit_user, content=request.POST.get('content'))
    comment.save()

    return HttpResponse(status=200)