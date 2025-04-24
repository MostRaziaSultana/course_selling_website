from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
# Create your models here.
class CourseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='courses/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class Coupon(models.Model):
    title = models.CharField(max_length=20, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_amount = models.PositiveIntegerField(default=500)
    used_by = models.ManyToManyField(User, blank=True, related_name='coupons_used')
    is_expired = models.BooleanField(default=False)
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
# Coupon expiry
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.end_date_time < timezone.now():
                self.is_expired = True
                print("Coupon is expired")
            else:
                self.is_expired = False
                print("Coupon is not expired")
        except:
            pass


class CoursePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_purchases')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_applied = models.CharField(max_length=50, null=True, blank=True)
    tran_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')  # 🔒 prevents duplicate purchases

    def __str__(self):
        return f"{self.user.username} purchased {self.course.title}"


class SiteSettings(models.Model):
    whatsapp_logo = models.ImageField(upload_to='logos/whatsapp', blank=True, null=True)
    facebook_pixel = models.CharField(max_length=255, blank=True, null=True)
    ssl_id = models.CharField(max_length=255, blank=True, null=True)
    ssl_password = models.CharField(max_length=255, blank=True, null=True)
    is_sandbox = models.BooleanField(default=True)

    def __str__(self):
        return f"Site Settings ({self.ssl_id})"

    def get_ssl_config(self):
        # Return a dictionary with SSL configuration
        return {
            'store_id': self.ssl_id,
            'store_pass': self.ssl_password,
            'issandbox': self.is_sandbox
        }