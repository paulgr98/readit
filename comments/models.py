from django.db import models
from users.models import ReaditUser
from submissions.models import Submission


# Create your models here.

class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(ReaditUser, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    content_html = models.TextField(blank=True, null=True)
