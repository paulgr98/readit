from django.db import models
from users.models import ReaditUser
from subreadits.models import Subreadit
from django.contrib.auth.models import User


# Create your models here.

class Submission(models.Model):
    title = models.CharField(max_length=255)
    subreadit = models.ForeignKey(Subreadit, on_delete=models.CASCADE)
    author = models.ForeignKey(ReaditUser, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    text = models.CharField(max_length=5000, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upvote_set = models.ManyToManyField(User, through='Upvote', related_name='upvote_set')

    def has_upvoted(self, user):
        return self.upvote_set.filter(user=user).exists()

    def __str__(self):
        return self.title


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upvote_by_user')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='upvotes_set')
    upvoted = models.BooleanField(default=False)
