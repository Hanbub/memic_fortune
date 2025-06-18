# memic_fortune

## Overview
`memic_fortune` is a Telegram bot that generates and sends meme-style fortune messages to users. It leverages Python and the Telegram Bot API to interact with users and deliver entertaining content.

## Features
- Sends random fortune messages in meme format
- Supports sticker and image responses
- Interactive buttons for user engagement

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/memic_fortune.git
   cd memic_fortune
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with your configuration variables. For example:
   ```env
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
   OTHER_CONFIG=your-other-config-value
   ```
   The bot will load environment variables from this file at startup.

## Usage

Run the bot with:
```sh
python bot.py
```

The bot will start and listen for messages on Telegram.

## File Structure

- `bot.py`: Main bot logic
- `requirements.txt`: Python dependencies
