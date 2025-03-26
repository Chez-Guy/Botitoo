import os
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo

class count_channel(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @app_commands.command(name="getcount",description="Get the current count in the counting channel.")
    async def slash_getcountcmd(self, interaction):
        await interaction.response.send_message("The current count in <#1136238325825536070> is __**{}**__".format(self.bot.getStorage("count")))

    @app_commands.command(name="set_count",description="Override the count in the counting channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(option="The number to set it to")
    async def slash_setcountcmd(self, interaction, option: int):
        self.bot.addToStorage("count", str(option))
        await interaction.response.send_message(":white_check_mark: <#1136238325825536070>'s count has successfully been changed to **{}**".format(self.bot.getStorage("count")), ephemeral=True)  
      
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(count_channel(bot=bot))