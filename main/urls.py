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

from django.urls import path
from . import views
from subreadits import views as sub_views
from users import views as user_views
from submissions import views as submission_views
from comments import views as comment_views

urlpatterns = [
    path('upvote/<submission_id>/', views.upvote, name='upvote'),
    path('upvote_unclicked/<submission_id>/', views.upvote_unclicked, name='upvote_unclicked'),
    path('downvote/<submission_id>/', views.downvote, name='downvote'),
    path('<int:submission_id>/comments/', views.comments_view, name='comments'),
    path('r/<str:name>/', sub_views.subreadit_view, name='subreadit'),
    path('user/<str:username>/', user_views.profile_view, name='profile'),
    path('', views.main_page_view, name="mainpage"),
    path('submit/<int:submission_id>', submission_views.create_or_edit_submission, name='create_or_edit_submission'),
    path('sign-in', user_views.sign_in, name='sign-in'),
    path('sign-out', user_views.sign_out, name='sign-out'),
    path('sign-up', user_views.sign_up, name='sign-up'),
    path('delete-submission', submission_views.delete_submission, name='delete_submission'),
    path('create-comment/<int:submission_id>', comment_views.create_comment, name='create_comment'),
    path('delete-comment', comment_views.delete_comment, name='delete_comment'),
]
