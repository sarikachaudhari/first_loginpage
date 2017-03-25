from django.db import models
from django.contrib.auth.models import User

class Registration(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(unique=True, max_length=30, null=False, blank=False)
    mobile_no = models.CharField(unique=True, max_length=10, null=False, blank=False)

    def __unicode__(self):
        return str(self.user.id)+ ' | '+str(self.user.username)

