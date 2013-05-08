from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

class Job(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    intern_project = models.BooleanField(_('Intern project?'))

class JobParameter(models.Model):
    container = models.ForeignKey(Job)
    name = models.CharField(max_length=255, db_index=True)
    value = models.CharField(max_length=255, db_index=True)
