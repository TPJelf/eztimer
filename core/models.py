from django.db import models
from django.contrib.auth.models import User
import zoneinfo
import datetime


class Timezone(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def utc_offset(self):
        tz = zoneinfo.ZoneInfo(self.name)
        now = datetime.datetime.now(tz)
        offset_hours = tz.utcoffset(now).total_seconds() / 3600
        return offset_hours


class UserProfile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Customer(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Task(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    allowed_users = models.ManyToManyField(User, related_name="allowed_tasks")

    def __str__(self):
        return self.name


class Action(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TimeEntry(models.Model):
    StatusTypes = (
        ("1", "Active"),
        ("s", "Submitted"),
        ("a", "Approved"),
        ("r", "Rejected"),
        ("x", "Recalled"),
    )

    # Try to fix this later.
    # class StatusTypes(models.TextChoices):
    #   ACTIVE = '1'
    #   SUBMITTED = 's'
    #   APPROVED = 'a'
    #   REJECTED = 'r'
    #   RECALLED = 'x'

    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=StatusTypes)

    def elapsed_time(self):
        return self.end_time - self.start_time

    def __str__(self):
        return (
            self.user.first_name + " " + self.user.last_name + " " + self.date_created
        )
