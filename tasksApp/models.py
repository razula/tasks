from django.db import models
from django.contrib.auth.models import AbstractUser


class UserBasic(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    # email = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.username


class Task(models.Model):
    
    status1 = "To do"
    status2 = "In progress"
    status3 = "Done"

    STATUS_CHOICES = [(status1, "To do"), (status2, "In progress"), (status3, "Done"),]

    category = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    dateCreated = models.CharField(max_length=256)
    dueDate = models.CharField(max_length=256)
    notes = models.CharField(max_length=256)
    status = models.CharField(max_length=256, choices=STATUS_CHOICES)
    users = models.ManyToManyField(UserBasic, related_name="tasks")

    
