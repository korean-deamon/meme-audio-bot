# 🎵 Meme Audio Bot

A powerful Telegram Inline Bot that allows you to search and send millions of meme sounds directly in any chat. The bot fetches live data from **MyInstants** and supports infinite scrolling.

## ✨ Features
- **Inline Mode**: Search and send sounds anywhere.
- **Infinite Scrolling**: Scroll through millions of sounds seamlessly.
- **Trending Sounds**: View popular memes even without a search query.
- **Optimized Performance**: Fast parsing using `lxml`.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- A Telegram Bot Token from [@BotFather](https://t.me/botfather) (Inline Mode must be **ON**)

### Telegram Bot Setup
Before running the bot, you must enable **Inline Mode** in BotFather:
1. Find [@BotFather](https://t.me/botfather) on Telegram.
2. Send `/setinline` command.
3. Select your bot from the list.
4. Enter a placeholder text (e.g., `Search for meme sounds...`).
5. Success! Your bot is now ready for inline queries.

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/korean-deamon/meme-audio-bot.git
   cd meme-audio-bot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file and add your token:
   ```env
   BOT_TOKEN=your_bot_token_here
   ```

### Running the Bot
```bash
python main.py
```

## 🛠 Built With
- [Aiogram 3.x](https://docs.aiogram.dev/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) with `lxml`
- [Httpx](https://www.python-httpx.org/)
