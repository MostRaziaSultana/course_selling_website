from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.hashers import make_password
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError


# models
from django.contrib.auth.models import User
from Home.models import Banner,Blog,BlogCategory,BusinessInfo,Logosettings,FAQ,Brand
from ContactUs.models import UserMessage
from Course.models import Coupon,SiteSettings,CourseCategory,CoursePurchase,Course

# forms
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name','is_staff')


class AddAdminUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password must contain at least 8 characters'}),
        required=True,
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters.')

        if password.isdigit():
            raise forms.ValidationError('Password cannot be entirely numeric.')

        common_passwords = ['123456', 'password', 'qwerty', 'letmein', 'admin', 'welcome', 'password123']
        if password.lower() in common_passwords:
            raise forms.ValidationError('Password is too common.')

        username = self.cleaned_data.get('username')
        if username and username.lower() in password.lower():
            raise forms.ValidationError('Password cannot be too similar to the username.')

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class UpdateAdminUserForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=False,
        label="Full Name",
        help_text="Enter both first and last name, or leave blank."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # Pre-fill full_name with first_name and last_name
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if full_name and len(full_name.split(' ')) < 2:
            raise forms.ValidationError("Please enter both first and last names or leave blank.")
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)

        user.password = self.instance.password

        full_name = self.cleaned_data.get('full_name', '').strip()
        if full_name:
            full_name_split = full_name.split(' ', 1)
            user.first_name = full_name_split[0]
            user.last_name = full_name_split[1] if len(full_name_split) > 1 else ""
        else:
            user.first_name = ""
            user.last_name = ""

        if commit:
            user.save()
        return user


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")

        if len(new_password) < 8:
            raise ValidationError("Password must contain at least 8 characters.")

        if new_password.isdigit():
            raise ValidationError("Password cannot be entirely numeric.")

        common_passwords = ['123456', 'password', 'qwerty', 'letmein', 'admin', 'welcome', 'password123']
        if new_password.lower() in common_passwords:
            raise ValidationError("Password is too common.")

        username = self.initial.get('username')
        if username and username.lower() in new_password.lower():
            raise ValidationError("Password cannot be too similar to the username.")

        return cleaned_data


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'description', 'image']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'image', 'content','show_on_homepage']

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']


class BusinessInfoForm(forms.ModelForm):
    class Meta:
        model = BusinessInfo
        fields = ['site_name', 'address', 'phone', 'email', 'copyright_year',
                  'instagram_link', 'facebook_link', 'youtube_link', 'linkedin_link','messenger_link',
            'twitter_link', 'whatsapp','telegram_link']


class LogosettingsForm(forms.ModelForm):
    class Meta:
        model = Logosettings
        fields = [
            'header_logo',
            'footer_logo',
            'favicon',
            'adminlogin_logo',
            'adminsidebar_logo'
        ]


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']



class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'logo', )


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'subject', 'message']


class CouponForm(forms.ModelForm):
    start_date_time = forms.DateTimeField()
    end_date_time = forms.DateTimeField()
    class Meta:
        model = Coupon
        fields = ('title', 'discount', 'minimum_amount', 'is_expired','start_date_time','end_date_time')

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ('whatsapp_logo', 'facebook_pixel','ssl_id','ssl_password','is_sandbox')

class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['name']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'image', 'price']

class CoursePurchaseForm(forms.ModelForm):
    class Meta:
        model = CoursePurchase
        fields = ['user', 'course', 'amount_paid', 'coupon_applied', 'is_ordered']