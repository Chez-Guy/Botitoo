import os
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo

class ping(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @commands.command(name="ping")
    async def pingcmd(self, interaction):
        await interaction.send("Pong!")
    
    @app_commands.command(name="ping",description="Send a simple ping command to our bot")
    async def slash_pingcmd(self, interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(ping(bot=bot))