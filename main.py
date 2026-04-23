import asyncio
import json
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultAudio
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    welcome_text = (
        "👋 **Welcome to Meme Audio Master!**\n\n"
        "Type `@` followed by my username in any chat to search sounds."
    )
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🚀 Try Inline Mode",
        switch_inline_query_current_chat=""
    ))
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    """
    Handle inline queries with Infinite Scroll (Pagination)
    Works for both specific search and empty (Trending) query.
    """
    query = inline_query.query.strip()
    offset = int(inline_query.offset) if inline_query.offset else 1
    
    # 1. Search MyInstants (fetches Trending if query is empty)
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
                performer=f"Trending • Page {offset}" if not query else f"Meme • Page {offset}"
            )
        )
    
    # If we have results, suggest next page for infinite scroll
    next_offset = str(offset + 1) if len(results_list) >= 20 else ""
    
    await inline_query.answer(
        results,
        cache_time=1,
        is_personal=False,
        next_offset=next_offset
    )

async def main() -> None:
    logger.info("Starting Meme Audio Master Bot (Clean Mode)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
