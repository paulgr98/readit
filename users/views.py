from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ReaditUser
from submissions.models import Submission

def profile_view(request, username):
    user = ReaditUser.objects.get(user__username=username)
    submissions = Submission.objects.filter(author_id=user.user_id)
    # sort sumbissions by created_at date
    submissions = sorted(submissions, key=lambda x: x.created_at, reverse=True)
    context = {'user': user, 'submissions': submissions}
    return render(request, 'public/profile.html', context)

def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

def sign_out(request):
    try:
        logout(request)
    except:
        return HttpResponse(status=400)
    return HttpResponse(status=200)

def sign_up(request):
    username = request.POST['username']
    if User.objects.filter(username=username).exists():
        return HttpResponse(status=400, content="User with provided username already exists")

    email = request.POST['email']
    if User.objects.filter(email=email).exists():
        return HttpResponse(status=400, content="User with provided email already exists")

    password = request.POST['password']
    user = User.objects.create_user(username, email, password)
    user.save()

    readit_user = ReaditUser(user=user)
    readit_user.save()

    return HttpResponse(status=200)
