import asyncio
import json
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultAudio
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web
from dotenv import load_dotenv

from scraper import search_myinstants

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    welcome_text = (
        "👋 **Welcome to Meme Audio Master!**\n\n"
        "I am an English-only Inline Bot connected directly to **MyInstants**. "
        "You can search and send millions of meme sounds in any chat!\n\n"
        "**How to use:**\n"
        "1. Type `@` followed by my username in any chat (e.g., `@MemeAudioMaster_bot `).\n"
        "2. Type the name of a meme to search (e.g., `ronaldo`, `bruh`).\n"
        "3. Click on the result to send the audio clip!\n\n"
        "Try it now by typing `@` and my name below!"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🚀 Try Inline Mode",
        switch_inline_query_current_chat=""
    ))
    
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.message(F.audio)
async def audio_handler(message: types.Message):
    """
    Handler to get file_id of any audio sent to the bot for local database building
    """
    file_id = message.audio.file_id
    title = message.audio.title or "Unknown Title"
    performer = message.audio.performer or "Unknown Performer"
    
    response = (
        f"✅ **Audio received!**\n"
        f"**Title:** `{title}`\n"
        f"**File ID:** `{file_id}`\n\n"
        f"You can add this to your `memes.json` for persistent storage."
    )
    await message.reply(response, parse_mode="Markdown")

@dp.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    """
    Handle inline queries with Infinite Scroll (Pagination)
    """
    query = inline_query.query.strip()
    # Get the current page from offset (default is 1)
    offset = int(inline_query.offset) if inline_query.offset else 1
    
    logger.info(f"Inline query: '{query}', Page: {offset}")
    
    # 1. Search MyInstants for the specific page
    results_list = await search_myinstants(query, page=offset)
    
    results = []
    seen_urls = set()
    for i, meme in enumerate(results_list):
        audio_url = meme.get("audio_url")
        if not audio_url or audio_url in seen_urls:
            continue
        seen_urls.add(audio_url)

        results.append(
            InlineQueryResultAudio(
                id=f"res_{offset}_{i}_{hash(audio_url)}",
                audio_url=audio_url,
                title=meme["title"],
                performer=f"Page {offset}"
            )
        )
    
    # If we got results, suggest the next page
    next_offset = str(offset + 1) if len(results_list) >= 10 else ""
    
    # Answer the inline query
    await inline_query.answer(
        results,
        cache_time=300,
        is_personal=False,
        next_offset=next_offset  # This enables infinite scroll
    )

async def handle(request):
    return web.Response(text="Bot is running!")

from aiogram.client.session.aiohttp import AiohttpSession

async def main() -> None:
    # Use a custom session with longer timeout for Hugging Face
    session = AiohttpSession(
        timeout=120, # 2 minutes
    )
    # Re-initialize bot with the custom session
    global bot
    bot = Bot(token=BOT_TOKEN, session=session)

    # Set up a dummy web server for Hugging Face health check
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 7860)
    
    logger.info("Starting health check server on port 7860...")
    asyncio.create_task(site.start())

    logger.info("Starting Meme Audio Master Bot (Live Website Search)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
