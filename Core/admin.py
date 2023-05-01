from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Center)
admin.site.register(Student)
admin.site.register(Coordinator)
admin.site.register(TimeSection)
admin.site.register(Attendance)
admin.site.register(Batch)
admin.site.register(Lead)
# admin.site.register(StudentAttendance)