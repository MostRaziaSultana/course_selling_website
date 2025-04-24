from django.db import models
from datetime import date
# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='sliders/')
    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    SHOW_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    title = models.CharField(max_length=200)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='blogs/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    show_on_homepage = models.CharField(max_length=3, choices=SHOW_CHOICES, default='no')

    def __str__(self):
        return self.title



def validate_year(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(f"The year {value} cannot be in the future.")
class BusinessInfo(models.Model):
    site_name = models.CharField(max_length=255, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    copyright_year = models.PositiveIntegerField(default=date.today().year, null=True, blank=True,
                                                 validators=[validate_year],
                                                 help_text="Year for copyright (cannot be in the future).")
    instagram_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    messenger_link = models.URLField(blank=True, null=True, verbose_name="Messenger Link")
    twitter_link = models.URLField(blank=True, null=True, verbose_name="Twitter Link")
    whatsapp = models.CharField(max_length=15, null=True, blank=True)
    telegram_link = models.URLField(blank=True, null=True, verbose_name="Telegram Link")

    def __str__(self):
        return "Business Info"

class Logosettings(models.Model):
    header_logo = models.ImageField(upload_to='logos/header/', blank=True, null=True)
    footer_logo = models.ImageField(upload_to='logos/footer/', blank=True, null=True)
    favicon = models.ImageField(upload_to='logos/favicon/', blank=True, null=True)
    adminlogin_logo = models.ImageField(upload_to='logos/adminlogin/', blank=True, null=True)
    adminsidebar_logo = models.ImageField(upload_to='logos/adminsidebar/', blank=True, null=True)

    def __str__(self):
        return "Logo Settings"



class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Brand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='brand_logos/')

    def __str__(self):
        return self.name


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    value = models.PositiveIntegerField()
    icon_class = models.CharField(max_length=50)

    def __str__(self):
        return self.name