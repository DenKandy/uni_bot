from bot.handlers.common import *
from bot.handlers import start, help, share

command_handlers = {
    # "name"        : __obj__
    Commands.start  : start.get_command_handler(),
    Commands.help   : help.get_command_handler(),

}

message_handlers = {
    # "name"        : __obj__
    Commands.all    : get_message_handler()

}


conversation_handlers = {
    # "name"        : __obj__
    Commands.share  : share.get_conversation_handler(),
}