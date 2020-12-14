from django.db import models

class GeneralUniModel(models.Model):
    welcome_message = models.CharField(max_length=150, db_index=True)
