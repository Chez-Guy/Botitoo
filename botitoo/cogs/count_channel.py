import os
import asyncio
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo

"""

This cog is for handling commands for a VIP only counting channel, as well as it's functions

"""

class count_channel(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @app_commands.command(name="get_count",description="Get the current count in the counting channel.")
    async def slash_getcountcmd(self, interaction):
        await interaction.response.send_message(f"The current count in <#{str(self.bot.count_channelID)}> is __**{self.bot.getStorage('count')}**__")

    @app_commands.command(name="set_count",description="Override the count in the counting channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(option="The number to set it to")
    async def slash_setcountcmd(self, interaction, option: int):
        self.bot.addToStorage("count", str(option))
        await interaction.response.send_message(f":white_check_mark: <#{str(self.bot.count_channelID)}>'s count has successfully been changed to **{self.bot.getStorage('count')}**", ephemeral=True)  
      
    
    # TODO: try to implement system to catch up once the bot goes offline then back online
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.channel.id == self.bot.count_channelID:
            try: 
              int(message.content)
            except:
              await message.delete()
              warningMsg = await self.bot.get_channel(self.bot.count_channelID).send(":warning: "+message.author.mention+" That is not the right number! :rage:")
              await asyncio.sleep(4)
              await warningMsg.delete()
            else:
              if int(message.content) == int(self.bot.getStorage("count"))+1:
                self.bot.addToStorage("count", int(self.bot.getStorage("count"))+1)
              else:
                await message.delete()
                warningMsg = await self.bot.get_channel(self.bot.count_channelID).send(":warning: "+message.author.mention+" That is not the right number! :rage:")
                await asyncio.sleep(4)
                await warningMsg.delete()
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(count_channel(bot=bot))