from django.contrib import admin

from .models import UserUniModel

class UserUniAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserUniModel, UserUniAdmin)
