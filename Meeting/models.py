from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField(verbose_name='آدرس اتاق')
    seats_count = models.IntegerField()


class MeetingManager(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=True)


class Meeting(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.PROTECT)
    start_time = models.DateTimeField(null=True, verbose_name='زمان شروع جلسه')
    end_time = models.DateTimeField(null=True, verbose_name='زمان اتمام جلسه')
    duration = models.IntegerField(null=True)
    meeting_manager = models.ForeignKey(to=MeetingManager, on_delete=models.PROTECT)
