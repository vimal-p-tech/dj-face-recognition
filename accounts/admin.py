from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)

admin.site.site_header ="Alpha Administration"
admin.site.index_title = 'Administration'                 # default: "Site administration"
admin.site.site_title = 'Team Alpha ' # default: "Django site admin"