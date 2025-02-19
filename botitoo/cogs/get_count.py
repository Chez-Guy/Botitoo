import os
from discord import app_commands
from discord.ext import commands
import asyncio
from botitoo.bot import Botitoo

class getCount(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @app_commands.command(name="count",description="Get the current count in the counting channel.")
    async def slash_countcmd(self, interaction):
        await interaction.response.send_message("> The current count is **{}**".format(int(self.bot.getStorage("count"))))

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(bot: Botitoo):
    await bot.add_cog(getCount(bot=bot))