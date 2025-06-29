import os
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import tasks, commands
from botitoo.bot import Botitoo

"""

Commands for registering custom roles to users so in case they stop subscribing, they lose their custom role
Then deletes the custom role after 15 days of no use

"""

class custom_role(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access


    # roles that cant be registered to a user in the db (admin roles, mod roles, etc.)
    # they're not actually given the roles but it's good to have this blacklist so there's no issues
    global blacklist
    blacklist = [
        1128048701953286192,
        1143002361913159701,
        1128048702024597538,
        1128048702024597534,
        1128048702024597536,
        1128048702024597537,
        1337157540055744655
    ]
    '''
    @app_commands.command(name="assign_role", description="Assign a custom role subscriber to their role. USE WITH **EXTREME** CAUTION!")
    @app_commands.describe(member="Member to link role to", role="Member's custom role to link.")
    #@app_commands.checks.has_role(1128048702024597536)
    @app_commands.checks.cooldown(1, 5000)
    async def assign(self, interaction, member: discord.Member, role: discord.Role):
        for r in range(0, len(blacklist)):
            if role.id == blacklist[r]:
                await interaction.response.send_message(f":warning: :warning: The role you are attempting to assign, {role.mention}, is blacklisted from being assigned. You can attempt to assign their custom role again **in 5 hours.** Be more vigilant next time! :angry:", silent=True, ephemeral=True)
                return
        await member.add_roles(role, reason="Moderator used /assign_role to assign this role to a user.")
        await interaction.response.send_message(f":white_check_mark: Successfully assigned {role.mention} to {member.mention}.", ephemeral=True)
    '''
    @app_commands.command(name="register_role", description="Register a custom role subscriber to their role, so if they unsubscribe, their role is removed.")
    @app_commands.describe(member="Member to link role to", role="Member's custom role to link.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def register(self, interaction, member: discord.Member, role: discord.Role):
        self.bot.cursor.execute(f"SELECT roleid FROM custom_roles WHERE userid={str(member.id)}")

        for i in blacklist:
            if role.id==i:
                await interaction.response.send_message(f":warning: User cannot be assigned role {role.mention}. Please be more cautious when attempting to register roles! :angry:", ephemeral=True)
                return


        if not self.bot.cursor.fetchone() and member.get_role(role.id):
            self.bot.cursor.execute(f"INSERT INTO custom_roles (userid, roleid) VALUES ({str(member.id)}, {str(role.id)})")
            self.bot.db.commit()
            await interaction.response.send_message(f":white_check_mark: **User {member.mention} has been successfully registered to role {role.mention}!**")
        elif not member.get_role(role.id):
            await interaction.response.send_message(f":warning: User {member.mention} has not been given the role {role.mention}. Please assign it to them then ", ephemeral=True)
        else:
            await interaction.response.send_message(f":warning: User {member.mention} has already been registered to role {role.mention}.", ephemeral=True)

    @tasks.loop(hours=1)
    async def check_invalid(self):
        results = self.bot.cursor.execute("SELECT invalid_time, roleid FROM custom_roles WHERE invalid=1")
        if self.bot.cursor.fetchall():
            for r in range(0, len(results)):
                if int(results[r][0]) + 1296000 <= datetime.now().timestamp(): # 15 day change
                    self.bot.cursor.execute(f"DELETE FROM custom_roles WHERE roleid={str(results[r][1])}")
                    await self.bot.get_guild(self.bot.guildID).get_role(int(results[r][1])).delete(reason="Role exceeded 15 day expiration")
                    self.bot.db.commit()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(custom_role(bot=bot))
        # change this ^^^ to the class above