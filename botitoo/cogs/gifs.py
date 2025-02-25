import os
import discord
from discord import app_commands
from discord.ext import commands

gifs = {
  "bleh":"https://cdn.discordapp.com/attachments/1241250107584680050/1252834482482839584/blehhcat.jpeg?ex=66745149&is=6672ffc9&hm=43f2212ea81163e0d2771202ed87e51d65d300e2b341545809bb4623069eaef4&",
  "uni":"https://cdn.discordapp.com/attachments/1220991843697819689/1252488526600212562/GQMevCVaEAAzkjf.png?ex=66746096&is=66730f16&hm=1f7656d1ef5b40cee6421d766853301f43dc3da153e377221882bc9efe955054&",
  "soggy":"https://cdn.discordapp.com/attachments/1220991843697819689/1252488552067891291/soggcyat.jpeg?ex=6674609c&is=66730f1c&hm=26ac31f957aa36e8d584ee5e95226b44f37916b0268ea7b1356d198a6a1e0d44&",
  "maxwell":"https://cdn.discordapp.com/attachments/1128048705363251265/1252498134475608135/9k.png?ex=66746989&is=66731809&hm=96de4524cf51fa8c8d32409e5a9ac5a5d7264f7bc7dcd4f8b1f3871ca93e53b8&",
  "glunglus":"https://cdn.discordapp.com/attachments/1128048705363251265/1252498219611590676/2Q.png?ex=6674699d&is=6673181d&hm=131a892d4ceb55d4610f88f744c8141d8a6a71ff3f83ba47b5ffb82cc4d58b6d&",
  "gruggy":"https://cdn.discordapp.com/attachments/1238704777383247894/1252501331738886257/image.png?ex=66746c83&is=66731b03&hm=47fc801142fdcbb66b87de840c468470ddaecac4699933db73ea2eae0398c258&",
  "crunchy":"https://cdn.discordapp.com/attachments/1238704777383247894/1252501542272241694/Z.png?ex=66746cb6&is=66731b36&hm=9d6a4578b6a55eeccaecead2cfea8b742d90cba7fedd75760178807b2b194091&",
  "zazu":"https://cdn.discordapp.com/attachments/1238704777383247894/1252502365756592138/6edc00bae1e8db8e7286ec4c3546b1ec.jpg?ex=66746d7a&is=66731bfa&hm=f3fe4e97f8fbc600f3a973de52035dc097c4755a972cf28996bfa969b3d1b189&",
  "indeed":"https://tenor.com/view/indeed-indeed-you-do-funny-memes-meme-gif-22592820"
}

class gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # adding a bot attribute for easier access
    
    @app_commands.command(name="gif", description="Sends a GIF selected by our amazing moderators to send in chat")
    @app_commands.checks.cooldown(1, 5)
    @app_commands.describe(option="The GIF you'd like to send in chat")
    @app_commands.choices(option=[app_commands.Choice(name=key, value=key) for key in gifs.keys()])
    async def _gif(self, interaction, option: app_commands.Choice[str]):
      value = gifs.get(option.value, ":warning: GIF not found!") 
      await interaction.response.send_message(value)
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded")

async def setup(bot):
    await bot.add_cog(gifs(bot=bot))