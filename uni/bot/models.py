from django.db import models

class UserUniModel(models.Model):
    telegram_id_str = 'telegram_id'
    user_types_str = 'user_types'

    STUDENT = 'student'
    TEACHER = 'teacher'
    MANAGEMENT = 'manager'
    ADMIN = 'admin'

    CHOICE_USER_TYPES = (
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподователь'),
        (MANAGEMENT, 'Дирекция'),
        (ADMIN, 'Админинстратор'))

    USER_TYPES_KEYS = {
        STUDENT     : CHOICE_USER_TYPES[0][1],
        TEACHER     : CHOICE_USER_TYPES[1][1],
        MANAGEMENT  : CHOICE_USER_TYPES[2][1],
        ADMIN       : CHOICE_USER_TYPES[3][1],
    }

    USER_TYPES_VALUES = {
        CHOICE_USER_TYPES[0][1] : STUDENT,
        CHOICE_USER_TYPES[1][1] : TEACHER,
        CHOICE_USER_TYPES[2][1] : MANAGEMENT,
        CHOICE_USER_TYPES[3][1] : ADMIN,
    }


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

    @staticmethod
    def get_users_by_category(category):
        from bot.models import UserUniModel
        db_users = UserUniModel.objects.all()
        user_ids = []
        if db_users:
            for db_user in db_users:
                user_type = getattr(db_user, UserUniModel.user_types_str)
                if user_type == category:
                    telegram_id = getattr(db_user, UserUniModel.telegram_id_str)
                    user_ids.append(int(telegram_id))
        
        return user_ids

