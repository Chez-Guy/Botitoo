import os
import discord
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo

# change this to the name of the cog
class cog(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @commands.command(name="hello")
    async def cmd(self, interaction):
        await interaction.send("Hello, {}!".format(interaction.user.mention))
    
    @app_commands.command(name="hello", description="Say hello to the user")
    async def slash_cmd(self, interaction):
        await interaction.response.send_message("Hello, {}!".format(interaction.user.mention))
    
    @commands.Cog.listener()
    async def on_message(self, message): # discord event function here
        print(message)
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(cog(bot=bot))
        # change this ^^^ to the class above