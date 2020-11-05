from chordium import Chordium

import os
from dotenv import load_dotenv

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
bot = Chordium("$", description="work in progress")
bot.run(TOKEN)