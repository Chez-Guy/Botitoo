import os
import discord
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo
import requests
import asyncio

class media_share(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    # make a confirm prompt? also make sure to change discord app commands perms so that only I can access :3
    @app_commands.command(name="start",description="Reset and start media share")
    @app_commands.checks.has_permissions(administrator=True)
    async def resetMediaShare(self, interaction):
        await interaction.response.send_message("__**Media Share Reset Initiated**__", ephemeral=True)
        await interaction.response.send_message("*Resetting submissions channel permission overrides...*", ephemeral=True)
        await self.bot.get_channel(1262608201082343424).set_permissions(self.bot.get_guild(1128048701387055209).default_role, view_channel=True)
        
        self.bot.cursor.execute("DELETE FROM media_share_users WHERE whitelisted=0")
        self.bot.db.commit()

        overwrites = self.bot.get_channel(1262608201082343424).overwrites

        for target in overwrites.items():
          if isinstance(target[0], discord.member.Member):
            await self.bot.get_channel(1262608201082343424).set_permissions(target[0], overwrite=None)
            await asyncio.sleep(1) # prevent rate limiting (i know yes there's other ways to do this)

        await interaction.response.send_message("__**Media Share Reset Complete!**__", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1262608201082343424 and not message.author.bot and not self.bot.changeMS_database("media_share_users", "read", message.author.id) == 3:
          if self.bot.validLink(message.content):
            index = message.content.find(self.bot.usedLink)
            indexAfter = index+len(self.bot.usedLink)
            videoID = message.content[indexAfter:indexAfter+11]

            if self.bot.changeMS_database("submissions", "read", videoID) < 5:
              url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id="+videoID+"&key="+os.getenv('GOOG_TOKEN')

              payload = {}
              headers = {
                'Accept': 'application/json'
              }

              response = requests.request("GET", url, headers=headers, data=payload).json()

              print(str(response["pageInfo"]["totalResults"]) + " video")
              if response["pageInfo"]["totalResults"] == 1:
                length = response['items'][0]['contentDetails']['duration'] # in ISO 8601 (https://en.wikipedia.org/wiki/ISO_8601#Durations)

                try:
                  if response['items'][0]['contentDetails']['contentRating']['ytRating'] == 'ytAgeRestricted':
                    await message.delete()
                    warningMsg = await self.bot.get_channel(1262608201082343424).send(":warning: "+message.author.mention+" That video is age restricted and cannot be added to the queue. Check <#1269852438379233360> for requirements")
                    await asyncio.sleep(7)
                    await warningMsg.delete()
                    return
                except: annadiow = 12 # idk, have to have an except for this shit

                if length.find("M") != -1: # -1 means it's not in there, hence it is < 1 minute
                  if length[length.find("M")-2] == "T" and int(length[length.find("M")-1]) == 1 and length.find("S") == -1: # length[length.find("M")-2] == "T" indicates the M value is < 10 minutes and exactly 1 minute
                    self.bot.addToMediaShare(response['items'][0]['id'])
                  else:
                    await message.delete()
                    warningMsg = await self.bot.get_channel(1262608201082343424).send(":warning: "+message.author.mention+" That video is invalid and cannot be added to the queue. Check <#1269852438379233360> for requirements")
                    await asyncio.sleep(7)
                    await warningMsg.delete()
                    return
                else:  
                  if length[length.find("S")-2] == "T": # less then 10 seconds
                    self.bot.addToMediaShare(response['items'][0]['id'])
                  else:
                    self.bot.addToMediaShare(response['items'][0]['id'])

              if not self.bot.checkWhitelist("media_share_users", message.author.id): 
                self.bot.changeMS_database("media_share_users", "write", message.author.id, 1)
              if not self.bot.checkWhitelist("submissions", videoID): 
                self.bot.changeMS_database("submissions", "write", videoID, 1)
              if self.bot.changeMS_database("media_share_users", "read", message.author.id) == 3:
                await self.bot.get_channel(1262608201082343424).set_permissions(message.author, view_channel=False, send_messages=False)
            else:
              await message.delete()
              warningMsg = await self.bot.get_channel(1262608201082343424).send(":warning: "+message.author.mention+" That video has been submitted too many times. Check <#1269852438379233360> for requirements")
              await asyncio.sleep(7)
              await warningMsg.delete()
          elif message.channel.id == 1262608201082343424 and not message.author.bot:
            if not self.bot.validLink(message.content):
              await message.delete()
              warningMsg = await self.bot.get_channel(1262608201082343424).send(":warning: "+message.author.mention+" The message you sent is invalid. Check <#1269852438379233360> for requirements")
              await asyncio.sleep(7)
              await warningMsg.delete()
              return

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(media_share(bot=bot))