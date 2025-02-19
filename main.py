import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
from botitoo.bot import Botitoo

bot = Botitoo()

try: 
    bot.run(bot.env["TOKEN"])
except discord.HTTPException as e:
    if e.status == 429: print("The Discord servers denied the connection for making too many requests :(")
    else: raise e
#bot.cursor.execute("DELETE FROM weirdos")
#bot.db.commit()