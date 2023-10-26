from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(teacher)
admin.site.register(contact)
admin.site.register(Course)
admin.site.register(Booking)
admin.site.register(Testimonial)