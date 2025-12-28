import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_TR_BOT_TOKEN")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TR_BOT_TOKEN not set")
if not AZURE_OPENAI_API_KEY:
    raise RuntimeError("AZURE_OPENAI_API_KEY not set")
if not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("AZURE_OPENAI_ENDPOINT not set")
if not AZURE_OPENAI_API_VERSION:
    raise RuntimeError("AZURE_OPENAI_API_VERSION not set")

#  USE AzureOpenAI
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
)

MODEL = "gpt-4.1"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def translate_to_persian(text: str) -> str:
    system_prompt = (
        "You are a native Persian speaker translating English to Persian.\n"
        "Style: informal, natural, conversational.\n"
        "No emojis. No symbols. No English.\n"
        "No explanations.\n"
        "Return only Persian text."
    )

    user_prompt = f"Translate this to informal Persian:\n{text}"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(e)
        return "Error in translation"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send any English text.\nI will translate it to Persian."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Usage:\nSend any English text.\nMax length: 4000 characters."
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "English to Persian translation bot.\nPowered by GPT-4.1."
    )


async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text or not text.strip():
        await update.message.reply_text("Empty message.")
        return

    if len(text) > 4000:
        await update.message.reply_text("Message too long.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    result = translate_to_persian(text)
    await update.message.reply_text(result)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(context.error)


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message)
    )

    app.add_error_handler(error_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
