import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive
load_dotenv()
token = os.getenv("MTMwOTYzODU5MDM2NzY2NjI1Nw.GLR9kO.47lTRhC1ZO2IBp6UOq0a-AMDCQVuGpp8Uu-vMY")


class MonBot(commands.Bot):
  async def setup_hook(self):
    for extension in ['games', 'moderation']:
      await self.load_extension(f'cogs.{extension}')

intents = discord.Intents.all()
bot = MonBot(command_prefix='!', intents=intents)

keep_alive()
bot.run(token=token)
