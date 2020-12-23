from django.db import models

class UserUniModel(models.Model):
    telegram_id_str = 'telegram_id'
    STUDENT = 'student'
    TEACHER = 'teacher'
    MANAGEMENT = 'managment'
    ADMIN = 'admin'

    CHOICE_USER_TYPES = (
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподователь'),
        (MANAGEMENT, 'Дирекция'),
        (ADMIN, 'Админинстратор'))

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6

    CHOICE_USER_COURSE = (
        (_0, 0),
        (_1, 1),
        (_2, 2),
        (_3, 3),
        (_4, 4),
        (_5, 5),
        (_6, 6))
       
    user_types = models.CharField(max_length=150, blank=True, default=STUDENT, choices=CHOICE_USER_TYPES)
    position_manager = models.CharField(max_length=150, db_index=True, blank=True, default='')
    curatorship = models.CharField(max_length=150, db_index=True, blank=True, default='')
    chair = models.CharField(max_length=150, db_index=True, blank=True, default='')
    course = models.IntegerField(db_index=True, blank=True,  default=_0, choices=CHOICE_USER_COURSE)
    group = models.CharField(max_length=150, db_index=True, blank=True, default='')
    full_name = models.CharField(max_length=150, db_index=True, default='')
    phone_number = models.CharField(max_length=50, db_index=True)
    telegram_id = models.CharField(max_length=50, db_index=True)
    is_active = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.full_name
