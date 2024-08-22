from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import datetime
# Create your models here.
class User(AbstractUser):
    is_student=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    def __str__(self): 
        return self.username

class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,limit_choices_to={'is_student':True})
    reg=models.CharField(max_length=10)
    col_name=models.CharField(max_length=50)
    parent=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    dept=models.CharField(max_length=50)
    pic = models.ImageField(upload_to='proimage', default='img_sample/avatar.png')

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):
    t_id=models.OneToOneField(User,on_delete=models.CASCADE,limit_choices_to={'is_teacher':True})
    dept=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    pic = models.ImageField(upload_to='proimage', default='img_sample/tavatar.png')
    def __str__(self):
        return (self.t_id.username)

class Subject(models.Model):
    sub=models.ForeignKey(TeacherProfile,on_delete=models.CASCADE)
    sub_name=models.CharField(max_length=50)
    semester=models.CharField(max_length=2)
    def __str__(self):
        return self.sub_name


class Attendance(models.Model):
    attend=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(default=datetime.date.today)
    time=models.TimeField()
    periods=models.IntegerField(default=0,null=True)
    subject=models.CharField(max_length=30,null=True,blank=True) 
    present=models.BooleanField(default=False)

    def __str__(self):
        return self.attend.username