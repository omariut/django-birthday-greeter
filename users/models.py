from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserTypeChoice(models.TextChoices):

        ADMIN = 'admin', _('admin')
        CUSTOMER = 'customer', _('customer')
        STUFF = 'stuff', _('stuff')

    email = models.EmailField(_("email address"), unique=True)
    first_name=models.CharField(max_length=20, blank=True,null=True)
    last_name=models.CharField(max_length=20, blank=True,null=True)
    user_type = models.CharField(max_length=50, choices=UserTypeChoice.choices, default=UserTypeChoice.CUSTOMER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


