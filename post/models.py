from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic

# Create your models here.

ext_validator = FileExtensionValidator(['pdf'])

def validate_type(file):
    accept = ['application/pdf']
    file_type = magic.from_buffer(file.read(1024), mime=True)
    if file_type not in accept:
        raise ValidationError("file type is not supported")

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    file = models.FileField(upload_to='papers/', validators=[ext_validator, validate_type])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title + '\n' + self.description
    
class Doc(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    processed_text = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.post_id

    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    post = models.ManyToManyField(Post)
    def __str__(self):
        return self.name