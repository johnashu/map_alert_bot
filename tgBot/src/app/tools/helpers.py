#
# By Maffaz 2021 - maffaz.one
#
from functools import wraps
import telegram

# Check out Version 20..
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func
