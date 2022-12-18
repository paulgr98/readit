from django.db import models
from users.models import ReaditUser
from subreadits.models import Subreadit

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

    def __str__(self):
        return self.title
