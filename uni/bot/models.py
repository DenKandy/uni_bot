from django.db import models

class GeneralUniModel(models.Model):
    field_name = 'welcome_message'
    welcome_message = models.TextField(db_index=True)
