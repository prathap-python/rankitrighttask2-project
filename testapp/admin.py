from django.contrib import admin
from testapp.models import Framework
class FrameworkAdmin(admin.ModelAdmin):
    list_display=['Url']
admin.site.register(Framework,FrameworkAdmin)

# Register your models here.
