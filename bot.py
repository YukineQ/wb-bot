import os
import logging
import redis
import traceback
import html
import json

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
)

import constants
from feedback.wb_feedback import Feedback
from excel import read_sheet

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

redis_db = redis.Redis(host='localhost', port=6379, decode_responses=True)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    await context.bot.send_message(
        chat_id=constants.DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


async def send_feedback_to_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    db_keys = redis_db.keys(pattern="*")

    for sku in _get_sku_list():
        await _send_feedback_for_all_chats(
            chat_ids=db_keys,
            sku=sku,
            context=context
        )


def _get_sku_list():
    df = read_sheet(os.getenv("EXCEL_FILE_PATH"))
    return df['SKU'].tolist()


async def _send_feedback_for_all_chats(
    chat_ids: list[str],
    *,
    sku: str,
    context: ContextTypes.DEFAULT_TYPE
):
    for chat in chat_ids:
        chat_id = redis_db.get(chat)

        await _send_feedback_message(
            sku=sku,
            chat_id=chat_id,
            context=context
        )


async def _send_feedback_message(
    sku: str,
    *,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    feedbacks = Feedback(sku)
    negative = feedbacks.negative_feedbacks().by_time(
        hours=constants.HOURS_BETWEEN_REPEAT).all()

    if not negative.feedbacks:
        return

    for feedback in negative.feedbacks:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Негативный отзыв \n"
            f"SKU: {feedbacks.get_sku()} \n"
            f"Оценка: {feedback.productValuation}/5 \n"
            f"{feedback.text} \n"
            f"Текущий рейтинг: {negative.valuation}"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    redis_db.set(chat_id, chat_id)

    await context.bot.send_message(
        update.effective_chat.id,
        text="Bot activated"
    )


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    redis_db.delete(chat_id)

    await context.bot.send_message(
        update.effective_chat.id,
        text="Bot deactivated"
    )


def main() -> None:

    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    job_queue = application.job_queue

    job_repeat = job_queue.run_repeating(
        send_feedback_to_chat,
        interval=60*60*constants.HOURS_BETWEEN_REPEAT,
        first=10
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("end", end))

    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
