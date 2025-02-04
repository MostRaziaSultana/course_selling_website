# Generated by Django 5.1.5 on 2025-01-29 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_remove_customuser_otp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(default='def.png', upload_to='profile_pics/')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verification_token', models.CharField(max_length=100, null=True)),
                ('password_reset_token', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
