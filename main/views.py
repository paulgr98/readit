from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from submissions.models import Submission, Upvote, Downvote
from comments.models import Comment
from users.models import ReaditUser
import markdown


def main_page_view(request):
    readit_user = None
    has_upvoted = False
    has_downvoted = False
    try:
        readit_user = ReaditUser.objects.get(id=request.user.id)
        has_upvoted = Upvote.objects.filter(user=request.user, upvoted=True).exists()
        has_downvoted = Downvote.objects.filter(user=request.user, downvoted=True).exists()
    except:
        pass

    submissions = Submission.objects.all()
    for submission in submissions:
        if not submission.text_html:
            text_html = markdown.markdown(submission.text)
            submission.text_html = text_html
            sub = Submission.objects.get(id=submission.id)
            sub.text_html = text_html
            sub.save()

    context = {
        'submissions': submissions,
        'readit_user': readit_user,
        'has_upvoted': has_upvoted,
        'has_downvoted': has_downvoted,
    }

    return render(request, 'public/mainpage.html', context)


def custom_404_view(request, exception):
    return render(request, 'public/not-found.html', status=404)


def upvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        author = ReaditUser.objects.get(id=submission.author.id)
        upvote_obj, created = Upvote.objects.get_or_create(user=request.user, submission=submission)
        if not created:
            if upvote_obj.upvoted:
                submission.upvotes -= 1
                author.karma -= 1
                upvote_obj.upvoted = False
            else:
                submission.upvotes += 1
                author.karma += 1
                upvote_obj.upvoted = True
        else:
            submission.upvotes += 1
            author.karma += 1
            upvote_obj.upvoted = True
        upvote_obj.save()
        submission.save()
        author.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def upvote_unclicked(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        author = ReaditUser.objects.get(id=submission.author.id)
        upvote_obj = Upvote.objects.filter(user=request.user, submission=submission).first()
        if upvote_obj:
            submission.upvotes -= 1
            author.karma -= 1
            submission.save()
            upvote_obj.delete()
            author.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Upvote does not exist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def downvote(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        author = ReaditUser.objects.get(id=submission.author.id)
        downvote_obj, created = Downvote.objects.get_or_create(user=request.user, submission=submission)
        if not created:
            if downvote_obj.downvoted:
                submission.downvotes -= 1
                author.karma += 1
                downvote_obj.downvoted = False
            else:
                submission.downvotes += 1
                author.karma -= 1
                downvote_obj.downvoted = True
        else:
            submission.downvotes += 1
            author.karma -= 1
            downvote_obj.upvoted = True
        downvote_obj.save()
        submission.save()
        author.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def downvote_unclicked(request, submission_id):
    if request.method == 'POST':
        submission = Submission.objects.get(id=submission_id)
        author = ReaditUser.objects.get(id=submission.author.id)
        downvote_obj = Downvote.objects.filter(user=request.user, submission=submission).first()
        if downvote_obj:
            submission.downvotes -= 1
            author.karma += 1
            submission.save()
            author.save()
            downvote_obj.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Upvote does not exist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def comments_view(request, submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        comments = Comment.objects.filter(submission=submission)

        for comment in comments:
            if not comment.content_html:
                content_html = markdown.markdown(comment.content)
                comment.content_html = content_html
                comm = Comment.objects.get(id=comment.id)
                comm.content_html = content_html
                comm.save()

        has_user_commented = False
        if request.user.is_authenticated:
            has_user_commented = any([comment.user.id == request.user.id for comment in comments])

        context = {'submission': submission, 'comments': comments, 'has_user_commented': has_user_commented}
        return render(request, 'public/comments.html', context)
    except:
        return render(request, 'public/not-found.html')
