import os
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import tasks, commands
from botitoo.bot import Botitoo

# change this to the name of the cog
class custom_role(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    @app_commands.command(name="register_role", description="Register a custom role subscriber to their role, so if they unsubscribe, their role is removed.")
    @app_commands.describe(member="Member to link role to", role="Member's custom role to link.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_cmd(self, interaction, member: discord.Member, role: discord.Role):
        self.bot.cursor.execute(f"SELECT userID FROM custom_roles WHERE userID={str(member.id)}")
        if not self.bot.cursor.fetchone():
            self.bot.cursor.execute(f"INSERT INTO custom_roles (userID, roleID) VALUES ({str(member.id)}, {str(role.id)})")
            self.bot.db.commit()
            await interaction.response.send_message(f":white_check_mark: **User {member.mention} has been successfully registered to role {role.mention}!**")
        else:
            await interaction.response.send_message(f":warning: User {member.mention} has already been registered to role {role.mention}.", ephemeral=True)

    @tasks.loop(hours=1)
    async def check_invalid(self):
        results = self.bot.cursor.execute("SELECT invalid_time, roleID FROM custom_roles WHERE invalid=1")
        if self.bot.cursor.fetchall():
            for r in range(0, len(results)):
                if int(results[r][0]) + 1296000 <= datetime.now().timestamp():
                    self.bot.cursor.execute(f"DELETE FROM custom_roles WHERE roleID={str(results[r][1])}")
                    await self.bot.get_guild(1128048701387055209).get_role(int(results[r][1])).delete(reason="Role exceeded 15 day expiration")
                    self.bot.db.commit()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(custom_role(bot=bot))
        # change this ^^^ to the class above