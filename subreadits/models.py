from django.db import models
from users.models import ReaditUser


# Create your models here.

class Subreadit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    owner = models.ForeignKey(ReaditUser, on_delete=models.CASCADE, related_name="subreadits")
    created_at = models.DateTimeField(auto_now_add=True)
    moderators = models.ManyToManyField(ReaditUser, related_name="moderated_subreadits", blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
