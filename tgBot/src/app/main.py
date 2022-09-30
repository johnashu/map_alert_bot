#
# By Maffaz 2021 - maffaz.one
#
from telegram.ext import (
    CommandHandler,
    filters,
    MessageHandler,
    CallbackContext,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from telegram.constants import ParseMode
from telegram import Update
from rpc.alert_api import get_map_data
from tools.helpers import *
from tools.utils import *
from includes.config import *
from messages.msg_templates import Templates

logging.info(f"{bot_name} Bot started")


class MapBot:
    # async def delete_in_q(self, update, context, delete_msg, m):
    #     # Not working on V20.. Check it out.. ..

    #     await context.bot.delete_message(
    #         chat_id=update.effective_chat.id, message_id=update.message.message_id
    #     )
    #     await context.job_queue.run_once(delete_msg, 10, context=m)

    async def delete_msg(self, context: CallbackContext):
        await context.bot.delete_message(
            chat_id=context.job.context.chat.id,
            message_id=context.job.context.message_id,
        )

    # @send_typing_action
    async def handle_msg(self, update, to_display, api_call):
        """Sends typing action while processing func command."""

        try:
            if api_call:
                to_display = ""
                msg = update.message
                update_id = update.update_id
                endpoint = msg.text[1:]

                res, data = get_map_data(endpoint, msg=msg, update_id=update_id)
                if res:
                    # to_display += "<code>"
                    if isinstance(data, dict):
                        for k, v in data.items():
                            to_display += f"<b>{k}</b>  ::  {v}\n"
                    # to_display += "</code>"
                else:
                    to_display += str(data)

            return to_display
        except Exception as e:
            return Templates.GenericError

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = open_file(help_msg_file)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = open_file(start_msg_file)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        err = Templates.error_reply(f"Update {update} caused error", context.error)
        logging.error(err)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=err,
        )

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I didn't understand that command.",
        )

    async def handle_endpoints(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        print(f"\n\nUpdate:\n{update}\n\nContext:{context}")
        to_display = await self.handle_msg(update, None, True)
        print(to_display)
        m = await context.bot.send_message(
            chat_id=update.effective_chat.id, text=to_display, parse_mode=ParseMode.HTML
        )
        # await self.delete_in_q(update, context, self.delete_msg, m)

    def main(self):
        application = ApplicationBuilder().token(envs.API_KEY).build()

        for c, m in list(MENU_ITEMS.items()):
            cmd = CommandHandler(c, self.__getattribute__(m))
            application.add_handler(cmd)

        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
        application.run_polling(stop_signals=None)


if __name__ == "__main__":
    MapBot().main()
