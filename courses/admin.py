from django.contrib import admin
from .models import User, Course, Order, Topic

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Order)
admin.site.register(Topic)
