import os
import discord
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo
import asyncio

# change this to the name of the cog
class simple_events(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    # this file is just for simple stuff that really doesn't need its own file for each, simplicity
    
    join_message = {} # make some shit here to pick from a random message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(1128048705363251265).send(f'yo everyone be quiet for a sec, {member.mention} just joined the server <:peepoSus:1141063962692169768> give them a warm welcome!! <:joecool:1141064043617059036>')

    # counting channel
    # TODO: try to implement system to catch up once the bot goes offline then back online
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.channel.id == 1136238325825536070:
            try: 
              int(message.content)
            except:
              await message.delete()
              warningMsg = await self.bot.get_channel(1136238325825536070).send(":warning: "+message.author.mention+" That is not the right number! :rage:")
              await asyncio.sleep(4)
              await warningMsg.delete()
            else:
              if int(message.content) == int(self.bot.getStorage("count"))+1:
                self.bot.addToStorage("count", int(self.bot.getStorage("count"))+1)
              else:
                await message.delete()
                warningMsg = await self.bot.get_channel(1136238325825536070).send(":warning: "+message.author.mention+" That is not the right number! :rage:")
                await asyncio.sleep(4)
                await warningMsg.delete()
    # (counting channel)

    # racist reactions checker
    # basically checks if N I and G letter emojis are in the same message's reactions. it's a little jank but it will save time
    # TODO: also apply it to special nitro reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
      
      if len(message.reactions) > 2:
        m = ""
        r = [] # for the individual reaction components (if needed to remove them later)
        for reaction in message.reactions:
          match reaction.emoji:
            case "🇳":
              m += "n"
              r.append(reaction)
            case "🇮":
              m += "i"
              r.append(reaction)
            case "🇬":
              m += "g"
              r.append(reaction)
        if m == "nig":
          for i in range(0, len(r)): # get each reaction component index
            users = [user async for user in r[i].users()]
            for user in users:
              await r[i].remove(user)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(simple_events(bot=bot))
        # change this ^^^ to the class above