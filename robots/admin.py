from django.contrib import admin
from .models import *


class RobotAdmin(admin.ModelAdmin):
    list_display = ("serial", "model", "version", "created")


admin.site.register(Robot, RobotAdmin)
