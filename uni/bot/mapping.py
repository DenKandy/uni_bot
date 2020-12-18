from bot.handlers import start

command_handlers = {
    # "name" : __func__
    start.StartCommand.NAME : start.StartCommand.executor,
}