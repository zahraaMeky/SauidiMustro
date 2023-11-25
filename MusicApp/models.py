from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import date

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    Full_name = models.CharField(max_length = 200)
    phone_no = models.CharField(max_length = 10)
    Photo = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
      return self.username
    
class teacher(models.Model):
    Full_name = models.CharField(max_length = 200)
    phone_no = models.CharField(max_length = 10)
    Photo = models.ImageField(upload_to='profile/', blank=True)
    experience = models.TextField()


    def __str__(self):
      return self.Full_name
    
class Course(models.Model):
    COURSE_CHOICES = (
    ("arabic", "عربية"),
    ("forign", "غربية"),

  )
    name = models.CharField(max_length = 50)
    description = models.TextField()
    img = models.ImageField(upload_to='courses/')
    type = models.CharField(max_length=9,choices=COURSE_CHOICES)
    price= models.IntegerField()
    teacher = models.ForeignKey(teacher,on_delete=models.CASCADE)
   
    def __str__(self):
      return self.name
    
class contact(models.Model):
    name = models.CharField(max_length = 50)
    messages = models.TextField()
    phone_no = models.CharField(max_length = 10)
    email = models.EmailField()
    type = models.CharField(max_length = 50)
    subject = models.CharField(max_length = 50)
   
   
    def __str__(self):
      return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return f"course {self.course} booked by  {self.user} on {date}"
    class Meta:
        ordering = ['-date']

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
      return self.message
    class Meta:
        ordering = ['-date']

    
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    Photo = models.ImageField(upload_to='blogs/', blank=True)
    description = models.TextField()


    def __str__(self):
      return self.title