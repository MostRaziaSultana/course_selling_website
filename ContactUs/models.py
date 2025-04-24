from django.db import models

# Create your models here.
class UserMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Messages"
    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactUs(models.Model):
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    hotline = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    support_mail = models.EmailField(max_length=40)

    def __str__(self):
        return self.address
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"