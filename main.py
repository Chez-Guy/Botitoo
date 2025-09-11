import discord
from botitoo.bot import Botitoo

bot = Botitoo()

try: 
    bot.run(bot.env["TOKEN"])
except discord.HTTPException as e:
    if e.status == 429: print("The Discord servers denied the connection for making too many requests :(")
    else: raise e