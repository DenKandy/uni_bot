import logging
from bot.handlers.common import *

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove

CATEGORY, CONTENT = range(2)

mapping_users_category = {}

def request_category(update: Update, context: CallbackContext) -> int:
    logging.info("Request category for sharing from user:{}".format(update.message.from_user))
    from bot.models import UserUniModel
    reply_keyboard = [[
        UserUniModel.USER_TYPES_KEYS[UserUniModel.STUDENT],
        UserUniModel.USER_TYPES_KEYS[UserUniModel.TEACHER],
        UserUniModel.USER_TYPES_KEYS[UserUniModel.MANAGEMENT] ]]

    update.message.reply_text(
        'Будь ласка виберіть категорію по якій буде розсилатися контент.'
        'Ви завжди можете закінчити спілкування з ботом шляхом введення наступної команди /{}.\n\n'.format(Commands.cancel),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CATEGORY

def cancel_sharing(update: Update, context: CallbackContext) -> int:
    logging.info("Finish sharing process from user:{}".format(update.message.from_user))
    if update.message.from_user.id in mapping_users_category:
        mapping_users_category.pop(update.message.from_user.id)

    update.message.reply_text(
        'Ви вийшли з діалогу з ботом', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def fail_unregistered(update: Update, context: CallbackContext) -> int:
    logging.info("Fail to start sharing process from user:{}, reason: unregistered user".format(update.message.from_user))
    update.message.reply_text(
        'Ви не можете розсилати повідомлення іншим')
    reply_registration_required(update, context, update.message.from_user)
    return cancel_sharing(update, context)

def fail_nousers(update: Update, context: CallbackContext) -> int:
    logging.info("Fail to start sharing process from user:{}, reason: no users in requested category".format(update.message.from_user))
    update.message.reply_text(
        'На жаль, немає користувачів в даній категорії')
    return cancel_sharing(update, context)

def start_sharing(update: Update, context: CallbackContext) -> int:
    logging.info("Start sharing process from user:{}".format(update.message.from_user))
    update.message.reply_text(
        'Бот дозволяє посилати такі файл як фото, повідомлення, і документи')

    if is_user_registered(update.message.from_user):
        return request_category(update, context)
    else:
        return fail_unregistered(update, context)

def receive_category(update: Update, context: CallbackContext) -> int:
    logging.info("Receive sharing category:{} from user:{}".format(update.message.text, update.message.from_user))
    from bot.models import UserUniModel
    category = UserUniModel.USER_TYPES_VALUES[update.message.text]
    mapping_users_category[update.message.from_user.id] = category

    if not UserUniModel.get_users_by_category(category):
        return fail_nousers(update, context)

    update.message.reply_text(
            f'Будь ласка надішліть фотографії, документи або повідомлення, щоб розіслати по заданій \'{update.message.text}\'категорії. \n'
            'Ви завжди можете закінчити спілкування з ботом шляхом введення наступної команди /{}.\n\n'.format(Commands.cancel),
            reply_markup=ReplyKeyboardRemove())
    
    return CONTENT

def share_content(update: Update, context: CallbackContext) -> int:    
    from bot.models import UserUniModel
    if update.message.from_user.id in mapping_users_category:
        telegram_users = UserUniModel.get_users_by_category(mapping_users_category[update.message.from_user.id])
        if telegram_users:
            for user_id in telegram_users:
                if not update.message.from_user.id == user_id:
                    logging.info("Try to share message: {} for user:{}".format(update.message, user_id))
                    if update.message.text:
                        update.message.bot.send_message(user_id, update.message.text)
                    if update.message.document:
                        update.message.bot.send_document(user_id, update.message.document, caption=update.message.caption)
                    if update.message.photo:
                        update.message.bot.send_photo(user_id, update.message.photo[-1], caption=update.message.caption)

            return request_category(update, context)
        else: 
            return fail_nousers(update, context)
    else:
        raise Exception("Incorrect condition")

def get_conversation_handler() -> ConversationHandler:
    from bot.models import UserUniModel
    return ConversationHandler(
        entry_points=[CommandHandler(Commands.share, start_sharing)],
        states={
            CATEGORY: [
                MessageHandler(
                    Filters.regex('^({}|{}|{})$'.format(
                        UserUniModel.USER_TYPES_KEYS[UserUniModel.STUDENT], 
                        UserUniModel.USER_TYPES_KEYS[UserUniModel.TEACHER], 
                        UserUniModel.USER_TYPES_KEYS[UserUniModel.MANAGEMENT])), receive_category), CommandHandler(Commands.cancel, cancel_sharing)],
            CONTENT: [
                CommandHandler(Commands.cancel, cancel_sharing),
                MessageHandler(Filters.document | Filters.photo | Filters.text, share_content)],
        },
        fallbacks=[CommandHandler(Commands.cancel, cancel_sharing)])







     



































# share_message_handler = None
# NAME_STUDENTS = "share_to_students"
# NAME_TEACHERS = "share_to_teachers"
# NAME_MANGERS = "share_to_managers"

# class Category:
#     student = 'student'
#     teacher = 'teacher'
#     manager = 'manager'

# class ShareCommand(IHandler):
#     NAME = 'share'
#     @staticmethod
#     def executor(update, context):
#         command = ShareCommand(update, context)
#         command.handle_safe(command.execute)

#     def __init__(self, update, context):
#         logging.info("Received -> {} comand to execute full text: {}".format(self.NAME, update.message.text))
#         IHandler.__init__(self, update, context)
    
#     def __reply_for_registered_user(self):
#         message = "Виберiть будьласка категорiю кому вiдправити: \n"
#         message = message + "Студентам /{}\n".format(NAME_STUDENTS)
#         message = message + "Вчителям /{}\n".format(NAME_TEACHERS)
#         message = message + "Дирекцii /{}\n".format(NAME_MANGERS)
#         self.update.message.reply_text(message)

#     def __reply_for_unregistered_user(self, user: User):
#         self.registration_required(user)
    
#     def execute(self):
#         if self.is_user_registered(self.update.message.from_user):
#             self.__reply_for_registered_user()
#         else:
#             self.__reply_for_unregistered_user(self.update.message.from_user)

# class EndShareCommand(IHandler):
#     NAME = 'endshare'
#     @staticmethod
#     def executor(update, context):
#         command = EndShareCommand(update, context)
#         command.handle_safe(command.execute)

#     def __init__(self, update, context):
#         logging.info("Received -> {} comand to execute full text: {}".format(self.NAME, update.message.text))
#         IHandler.__init__(self, update, context)
    
#     def __reply_for_registered_user(self):
#         share_message_handler.end_share(self.update.message.from_user.id)

#     def __reply_for_unregistered_user(self, user: User):
#         self.registration_required(user)
    
#     def execute(self):
#         if self.is_user_registered(self.update.message.from_user):
#             self.__reply_for_registered_user()
#         else:
#             self.__reply_for_unregistered_user(self.update.message.from_user)


# class ShareCategoryHandlerBase(IHandler):
#     @staticmethod
#     def command_student_handler(update, context):
#         command = ShareCategoryHandlerBase(update, context, NAME_STUDENTS, Category.student)
#         command.handle_safe(command.execute)
#         share_message_handler.start_share(update.message.from_user.id, command)
    
#     @staticmethod
#     def command_teacher_handler(update, context):
#         command = ShareCategoryHandlerBase(update, context, NAME_TEACHERS, Category.teacher)
#         command.handle_safe(command.execute)
#         share_message_handler.start_share(update.message.from_user.id, command)
    
#     @staticmethod
#     def command_management_handler(update, context):
#         command = ShareCategoryHandlerBase(update, context, NAME_MANGERS, Category.manager)
#         command.handle_safe(command.execute)
#         share_message_handler.start_share(update.message.from_user.id, command)
    
#     @staticmethod
#     def get_users_by_category(category):
#         from bot.models import UserUniModel
#         db_users = UserUniModel.objects.all()
#         user_ids = []
#         if db_users:
#             for db_user in db_users:
#                 user_type = getattr(db_user, UserUniModel.user_types_str)
#                 if user_type == category:
#                     telegram_id = getattr(db_user, UserUniModel.telegram_id_str)
#                     user_ids.append(int(telegram_id))
        
#         return user_ids

#     def share(self, update, context):
#         ids = ShareCategoryHandlerBase.get_users_by_category(self.category)

#         if ids:
#             for user_id in ids:
#                 if not update.message.from_user.id == user_id:
#                     if update.message.text:
#                         update.message.bot.send_message(user_id, update.message.text)
#                     if update.message.document:
#                         self.update.message.bot.send_document(user_id, update.message.document, caption=update.message.caption)
#                     if update.message.photo:
#                         self.update.message.bot.send_photo(user_id, update.message.photo[0], caption=update.message.caption)
                
#                     logging.info("Send message {} to user {}".format(update.message, user_id))
#         else: 
#             raise HandlerException("Немаэ користувачив запрошенной категорii")

#     def __init__(self, update, context, name, category):
#         logging.info("Received -> {} comand to execute full text: {}".format(name, update.message.text))
#         IHandler.__init__(self, update, context)
#         self.category = category
#         self.name = name
    
#     def __reply_for_registered_user(self):
#         self.update.message.reply_text('Вiдправте контент боту для того щоб його розicлати категорi {}.'.format(self.category))

#     def __reply_for_unregistered_user(self, user: User):
#         self.registration_required(user)
    
#     def execute(self):
#         if self.is_user_registered(self.update.message.from_user):
#             self.__reply_for_registered_user()
#         else:
#             self.__reply_for_unregistered_user(self.update.message.from_user)

# class ShareMessageHandler(IHandler):
#     def __init__(self, update, context):
#         IHandler.__init__(self, update, context)
#         self.chats = {}

#     def start_share(self, user_id, share_obj):
#         if user_id in self.chats:
#             logging.warning("The sharing process is already started user:{}, message:{}".format(user_id, share_obj.update.message))
#         logging.info("The sharing process is requested by user:{}, message:{}".format(user_id, share_obj.update.message))
#         self.chats[user_id] = share_obj
    
#     def end_share(self, user_id):
#         if user_id in self.chats:
#             logging.info("The end of sharing process is requested by user:{}".format(user_id)) 
#             self.chats.pop(user_id)
#         else:
#             logging.warning("The sharing is not started user:{}".format(user_id)) 

#     def handle_share(self):
#         user_id = self.update.message.from_user.id
#         if user_id in self.chats:
#             logging.info("Share message:{} by user:{}".format(self.update.message, self.update.message.from_user))
#             self.chats[user_id].share(self.update, self.context)
#         else:
#            logging.warning("The sharing is not started user:{}, message:{}".format(self.update.message.from_user, self.update.message))
    


# share_message_handler = ShareMessageHandler(None, None)

# def share_message_handle(update, context):
#     share_message_handler.update = update
#     share_message_handler.context = context
#     share_message_handler.handle_safe(share_message_handler.handle_share)