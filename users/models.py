from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ReaditUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    about_text = models.TextField(blank=True, null=True, max_length=500, help_text="Tell us about yourself",
                                  verbose_name="About", default="")
    avatar_url = models.URLField(blank=True, null=True, max_length=500,
                                 verbose_name="Avatar URL", default="")
    karma = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

