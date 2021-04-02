from chordium import Chordium

import os
from dotenv import load_dotenv

import logging

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
bot = Chordium("$", description="work in progress")

bot.logger = logging.getLogger(__name__)
bot.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("{asctime} - {levelname} - {message}", style="{")
)
bot.logger.addHandler(handler)
bot.logger.info("Instance starting...")

bot.run(TOKEN)