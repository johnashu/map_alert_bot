#
# By Maffaz 2021 - maffaz.one
#
from time import sleep
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler,
    CallbackContext,
)
from telegram import ParseMode
from rpc.alert_api import get_map_data
from tools.helpers import *
from tools.utils import *
from includes.config import *
from messages.msg_templates import Templates


logging.info(f"{bot_name} Bot started")


def delete_msg(context: CallbackContext):
    context.bot.delete_message(
        chat_id=context.job.context.chat.id, message_id=context.job.context.message_id
    )


@send_typing_action
def handle_msg(update, context, to_display, api_call):
    """Sends typing action while processing func command."""
    print(
        f"\n\nUpdate:\n{update}\n\nContext:\n{context}\n\nupdate.message.text:\n{update.message.text}"
    )
    if api_call:
        to_display = ""
        msg = update.message
        params = [{"user_id": msg.chat.id}]
        update_split = msg.text[1:].split()

        endpoint = update_split[0]
        if len(update_split) > 1:
            params.update({"params": update_split[1:]})

        print("endpoint", endpoint)

        res, data = get_map_data(endpoint, params=params)
        if res:
            to_display += "<code>"
            for k, v in data.items():
                to_display += f"{k}  ::  {v}\n"
            to_display += "</code>"

    m = context.bot.send_message(
        chat_id=update.effective_chat.id, text=to_display, parse_mode=ParseMode.HTML
    )

    delete_in_q(update, context, delete_msg, m)


def delete_in_q(update, context, delete_msg, m):
    # This is a blocking call..
    # Messages should delete instantly if used?? Maybe TG limits this?.

    context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )

    context.job_queue.run_once(delete_msg, 10, context=m)


def help_command(update, context):
    msg = open_file(help_msg_file)
    context.dispatcher.run_async(handle_msg, update, context, msg, False)


def start_command(update, context):
    msg = open_file(start_msg_file)
    context.dispatcher.run_async(handle_msg, update, context, msg, False)


def endpoint_commands(update, context):
    context.dispatcher.run_async(handle_msg, update, context, None, True)


def error(update, context):
    logging.info(f"Update {update} caused error {context.error}")


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def main():
    updater = Updater(envs.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help_command, run_async=True))
    dp.add_handler(CommandHandler("start", start_command, run_async=True))

    for c in list(ENDPOINTS.keys()):
        dp.add_handler(CommandHandler(c, endpoint_commands, run_async=True))

    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling(10)
    updater.idle()


main()
