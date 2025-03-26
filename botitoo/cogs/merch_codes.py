import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
from botitoo.bot import Botitoo


# change this to the name of the cog
class merch_codes(commands.Cog):
    def __init__(self, bot: Botitoo):
        self.bot = bot # adding a bot attribute for easier access

    async def getCode(self, interaction):
        roles = interaction.guild.get_member(interaction.user.id).roles
        for role in range(0, len(roles)):
            if roles[role].id == 1138520134118559886 or roles[role].id == 1138520134118559888: # Chez chad role and $500 role
                print("user valid")
                self.bot.cursor.execute("SELECT date FROM code_users WHERE id={}".format(str(interaction.user.id)))
                result = self.bot.db.cursor.fetchone()[0]

                if result:
                    '''
                    compare the dates using Unix Epoch time, if the difference between the epoch time saved in the database and the current epoch time is greater then 
                    however many seconds are in a month, then its fine to give them another code. are there better ways to do this? yes. am i too lazy to find them out? yes.
                    '''
                    if result - int(datetime.now().timestamp()) >= 2629743:
                        prompt = "UPDATE code_users SET date = {0} WHERE id = {1}".format(str(datetime.now().timestamp()), interaction.user.id)
                    else:
                        await interaction.response.send_message(":warning: You are not yet able to claim another code. Your next code will become available on <t:{}:F>.".format(str(result + 2629743)), ephemeral=True)
                        break
                else:
                    prompt = "INSERT INTO code_users (id, date) VALUES ({0}, {1})".format(str(interaction.user.id), str(int(datetime.now().timestamp())))

                self.bot.cursor.execute("SELECT * FROM discount_codes ORDER BY RAND() LIMIT 1")
                code = self.bot.cursor.fetchone()[0]
                oneMonth = int(datetime.now().timestamp()) + 2629743 # one month (~30.4 days) from now in seconds (for epoch time)
                await interaction.response.send_message(":gift: Here's your discount code: __**{0}**__ :gift: You can claim another code on <t:{1}:F>! *(~30 days from now)* Make sure to either __use it now or write it down__ because **this code will only display in this chat for 15 minutes.**\n\nYour code can be applied in checkout at the [merch site](https://chez.shop).".format(code, str(oneMonth)), ephemeral=True)
                
                #self.bot.cursor.execute("DELETE FROM discount_code WHERE code={code}")
                # uncomment this line when it's been verified that it works
                
                self.bot.cursor.execute(prompt)
                return
        # this will go if they don't have the role (atleast it should anyways)
        await interaction.response.send_message(":warning: You are not eligible to recieve a discount code. You must be in the <@&1138520134118559886> YouTube Membership tier. You can change that by visiting", ephemeral=True)

    @app_commands.command(name="send_discount_code")
    @app_commands.checks.has_permissions(administrator=True)
    async def sendEmbed(self, interaction):

        #TODO: figure out how to make it fetch the existing message instead of making a new one every time

        embed = discord.Embed(
            title="How do I get a discount on merch??",
            description="YouTube Channel Members in the <@&1138520134118559886> tier can claim a discount code which gives 20% off their entire cart on the [merch site](https://chez.shop)! Each member can only claim **1 code per month**. Your code will appear in this chat, then **it will dissapear after 15 minutes**, so make sure to write it down!\n\n> Become a YouTube Member to the chezitoo channel [here](<https://www.youtube.com/channel/UCa6E2JD9uBHUSLupI8q26kQ/join>). You must purchase the Chez Chad role in order to access discount codes.\n> Learn how to connect your YouTube account to your discord [here](<https://chez.shop/pages/yt-discord-link>)",
            color=5814783
        )
        embed.set_footer(text="Learn more about becoming a YouTube Member here: https://www.youtube.com/@chezitoo/join. You must purchase the Chez Chad role in order to claim")

        button = Button(label="Claim a code", style=discord.ButtonStyle.primary)

        async def get_code_ctx(ctx): 
            await self.getCode(ctx)

        button.callback = get_code_ctx

        view = View().add_item(button)

        await self.bot.get_channel(1291280916953698386).send(embed=embed, view=view)
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot: Botitoo):
    await bot.add_cog(merch_codes(bot=bot))
        # change this ^^^ to the class above