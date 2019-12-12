from django.contrib import admin

# Register your models here.
from app01.models import *
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','username','password','telephone']
    list_editable = ['username','password','telephone']


admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(Customer)
admin.site.register(Campuses)
admin.site.register(ClassList)
admin.site.register(ConsultRecord)
admin.site.register(Enrollment)
admin.site.register(CourseRecord)
admin.site.register(StudyRecord)