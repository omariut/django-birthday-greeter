from django.db import models
import pytz
from django.contrib.auth import get_user_model
User=get_user_model()

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.RESTRICT)
    birthdate = models.DateField()
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.user.first_name + self.user.last_name

    def __str__(self):
        return self.user.username