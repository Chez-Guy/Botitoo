import os
import discord
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo
import asyncio

"""

For simple events and stuff I didn't want to make into separate scripts

"""

class simple_events(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access
    
    join_message = {} # TODO: make some different messages here to pick at random
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(self.bot.general_chatID).send(f'yo everyone be quiet for a sec, {member.mention} just joined the server <:peepoSus:1141063962692169768> give them a warm welcome!! <:joecool:1141064043617059036>')

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