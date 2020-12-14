from django.contrib import admin

from .models import GeneralUniModel

class GeneralUniAdmin(admin.ModelAdmin):
    pass

admin.site.register(GeneralUniModel, GeneralUniAdmin)
