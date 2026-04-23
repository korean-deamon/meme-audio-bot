---
title: Meme Audio Bot
emoji: 🎵
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# 🎵 Meme Audio Bot

A powerful Telegram Inline Bot that allows users to search and send millions of meme sounds directly in any chat. The bot fetches live data from **MyInstants** and supports infinite scrolling.

## ✨ Features
- **Inline Mode**: Search and send sounds anywhere.
- **Infinite Scrolling**: Scroll through hundreds of results seamlessly.
- **Live Search**: Fetches the latest trending sounds from MyInstants.
- **Hugging Face Ready**: Optimized for deployment on Hugging Face Spaces.

## 🚀 Setup & Deployment

### Local Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create `.env` and add `BOT_TOKEN`.
4. Run `python main.py`.

### Hugging Face Deployment
1. Create a new **Docker** Space on Hugging Face.
2. Upload all files from this repository.
3. In **Settings > Variables and secrets**, add your `BOT_TOKEN`.
4. The bot will automatically build and start!

---
*Built with Aiogram 3.x and Beautiful Soup 4.*
