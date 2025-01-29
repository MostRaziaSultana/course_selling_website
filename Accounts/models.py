from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default= 'def.png')
    phone_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100,null=True)
    password_reset_token = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'