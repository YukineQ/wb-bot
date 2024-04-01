import logging

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
)

import constants
from config import config
from feedback.wb_feedback import Feedback
from core.helpers.excel import read_sheet
from core.helpers.cache import Cache
from chat_bot.error_handler import error_handler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def send_feedback_to_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    chats = await Cache.backend.get_keys()

    for sku in _get_sku_list():
        await _send_feedback_for_all_chats(
            chats=chats,
            sku=sku,
            context=context
        )


def _get_sku_list():
    df = read_sheet(config.EXCEL_FILE_PATH)
    return df['SKU'].tolist()


async def _send_feedback_for_all_chats(
    chats: list[str],
    *,
    sku: str,
    context: ContextTypes.DEFAULT_TYPE
):
    for key in chats:
        chat_id = await Cache.backend.get(key=key)

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
    negative_feedback_obj = Feedback(sku).negative_feedbacks().by_time(
        hours=constants.HOURS_BETWEEN_REPEAT
    ).all()
    negative_feedback_list = negative_feedback_obj.feedbacks

    if not negative_feedback_list:
        return

    for feedback in negative_feedback_list:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Негативный отзыв \n"
            f"SKU: {sku} \n"
            f"Оценка: {feedback.productValuation}/5 \n"
            f"{feedback.text} \n"
            f"Текущий рейтинг: {negative_feedback_obj.valuation}"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    await Cache.backend.set(key=chat_id, val=chat_id)

    await context.bot.send_message(
        update.effective_chat.id,
        text="Bot activated"
    )


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    await Cache.backend.delete(key=chat_id)

    await context.bot.send_message(
        update.effective_chat.id,
        text="Bot deactivated"
    )


def run_bot() -> None:
    application = Application.builder().token(config.BOT_TOKEN).build()

    job_queue = application.job_queue

    job_repeat = job_queue.run_repeating(
        send_feedback_to_chat,
        interval=constants.HOURS_BETWEEN_REPEAT * 60 * 60,
        first=10
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("end", end))

    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
