import os
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from botitoo.bot import Botitoo

# change this to the name of the cog
class role_changes(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    # TODO: find a better way to do this. prolly taking up some memory, i dunno

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles): # if roles are added        
            roles = [
                "YouTube Member", 
                "LV50 - Godly Chatter", 
                "LV60 - Ungodly Chatter",
                "LV100 - Supreme Chatter"
            ]

            announcement = {
                "YouTube Member": "a YouTube Member", 
                "LV50 - Godly Chatter": "Chatter Level 50", 
                "LV60 - Ungodly Chatter": "Chatter Level 60",
                "LV100 - Supreme Chatter": "Chatter Level 100"
            }
            
            for role in roles:
              for i in range(0, len(before.roles)):
                if before.roles[i].name == role:
                  isRole = True
                  break
                else:
                  isRole = False
              if not isRole:
                for i in range(0, len(after.roles)):
                  if after.roles[i].name == role:  
                    await self.bot.get_channel(1194447194137297129).send(f'{after.mention} just became a {announcement[role]}!')
                    if role == "LV60 - Ungodly Chatter": await self.bot.get_channel(1194447194137297129).send("Now they can change the <@&1128048702024597540> role color for **1 day!!**, send a DM to <@1297779124739510353> and let us know your color of choice!")
                    elif role == "LV100 - Supreme Chatter": await self.bot.get_channel(1194447194137297129).send("Now they can have **their own custom role!** Send a DM to <@1297779124739510353> and let us know your role name and icon of choice!")
                    # maybe add this onto the top message? dk
                    break

            # TODO: check if someone resubs. if the sub role is added AND if they're in the database AND their role is marked as invalid, remove the invalid
            if after.get_role(1345992570601209890) and not before.get_role(1345992570601209890):
              self.bot.cursor.execute(f"SELECT * FROM custom_roles WHERE userID={str(after.id)} AND invalid=1")
              if self.bot.cursor.fetchone():
                self.bot.cursor.execute(f"UPDATE custom_roles SET invalid=0 WHERE userID={str(after.id)}")
                self.bot.db.commit()

        else: # if roles are removed
        
            # --- check if booster ---
            for i in range(0, len(before.roles)):
              #  vvvvvvvvvv this might be messy if they're a member AND booster. figure out this logic someday to make sure it's sound
              if before.roles[i].name == "Server Booster" or before.roles[i].name == "YouTube Member":
                for i in range(0, len(after.roles)):
                  if after.roles[i].name == "Server Booster" or before.roles[i].name == "YouTube Member":
                    isBooster = True
                    break
                  else: 
                    isBooster = False
                break
              else: 
                isBooster = False
            if not isBooster:
              for i in range(0, len(after.roles)):
                for i2 in range(0, len(self.bot.colors)):
                  if after.roles[i].id == self.bot.colors[i2]:
                    await after.remove_roles(after.guild.get_role(self.bot.colors[i2]))
                    await self.bot.get_channel(1321148137494020157).send(f'Removed color roles from {after.mention}')
                    isBooster = False # remember to set this as false cause could cause issues
                    break

              # TODO: change all of these to after.get_role(roleID) cuz i JUST discovered that. they werent lying when they said autism speaks

            # --- check if custom role subscriber ---
            if not after.get_role(1345992570601209890) and before.get_role(1345992570601209890): 
              self.bot.cursor.execute(f"SELECT roleID FROM custom_roles WHERE userID={str(after.id)}")
              roleID = self.bot.cursor.fetchone()[0]
              await after.remove_roles(int(roleID))
              self.bot.cursor.execute(f"UPDATE custom_roles SET invalid=1, invalid_time={str(int(datetime.now().timestamp()))} WHERE userID={str(after.id)}")
              self.bot.db.commit()
              await self.bot.get_channel(1321148137494020157).send(f'Removed custom role {self.bot.get_guild(1128048701387055209).get_role(int(roleID)).mention} from {after.mention}.')

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(role_changes(bot=bot))
        # change this ^^^ to the class above