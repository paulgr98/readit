"""readit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path
from django.urls import path
from . import views
from subreadits import views as sub_views
from users import views as user_views

urlpatterns = [
    path('upvote/<submission_id>/', views.upvote, name='upvote'),
    path('upvote_unclicked/<submission_id>/', views.upvote_unclicked, name='upvote_unclicked'),
    path('downvote/<submission_id>/', views.downvote, name='downvote'),
    path('<int:submission_id>/comments/', views.comments_view, name='comments'),
    path('r/<str:name>/', sub_views.subreadit_view, name='subreadit'),
    path('user/<str:username>/', user_views.profile_view, name='profile'),
    re_path(r'^$', views.main_page_view, name="mainpage"),
]
