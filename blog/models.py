from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
class Post(models.Model):
    
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    content = RichTextField(blank = True, null = True)
    visible = models.BooleanField(default=False)
    
    
    upload = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return self.title

class PostComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp= models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.post)
    

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username