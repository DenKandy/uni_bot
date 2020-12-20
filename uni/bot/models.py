from django.db import models

class GeneralUniModel(models.Model):
    field_name = 'welcome_message'
    welcome_message = models.TextField(db_index=True)

class UserUniModel(models.Model):
    STUDENT = 'Студент'
    TEACHER = 'Преподователь'
    MANAGEMENT = 'Дирекция'
    ADMIN = 'Админинстратор'

    CHOICE_USER_TYPES = (
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподователь'),
        (MANAGEMENT, 'Дирекция'),
        (ADMIN, 'Админинстратор'),
        )

    user_types = models.CharField(max_length=150, blank=True, default=STUDENT, choices=CHOICE_USER_TYPES)
    position_manager = models.CharField(max_length=150, db_index=True, blank=True, default='')
    curatorship = models.CharField(max_length=150, db_index=True, blank=True, default='')
    chair = models.CharField(max_length=150, db_index=True, blank=True, default='')
    course = models.IntegerField(db_index=True, blank=True, default=0)
    group = models.CharField(max_length=150, db_index=True, blank=True, default='')
    full_name = models.CharField(max_length=150, db_index=True, default='')
    phone_number = models.CharField(max_length=50, db_index=True)
    telegram_id = models.CharField(max_length=50, db_index=True)

