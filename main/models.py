from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    work_at = models.CharField(max_length=50, null=True, blank=True)
    intro = models.TextField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.user.username
    
