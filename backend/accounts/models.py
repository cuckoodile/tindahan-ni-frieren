from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.formatters import formatName
from utils.validators import validate_file_size
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True)
    profile = models.ImageField(
        upload_to='profile/', 
        validators=[validate_file_size],
        help_text='Max file size is 5 MB',
        error_messages={
            'invalid': "Image files only with maximum of 5 MB."
        },
        default='profile/default.jpg',
        blank=True
    )
    phone_number = PhoneNumberField(
        region='PH',
        help_text="Philippine mobile number (e.g. +639123456789 or 09123456789)",
        error_messages={
            'invalid': "Enter a valid Philippine phone number."
        }
    )


    def save(self, *args, **kwargs):
        self.first_name = formatName(self.first_name)
        self.last_name = formatName(self.last_name)
        self.middle_name = formatName(self.middle_name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username