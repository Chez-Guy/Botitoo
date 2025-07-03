import os
import json
import discord
from discord.ext import commands
from dotenv import dotenv_values
import glob
import psycopg

"""

Main script that defines the Botitoo class, all its vairables, functions, and some event listeners

"""

class Botitoo(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.integrations = True
        intents.reactions = True
        
        self.env = dotenv_values("../botitoo/.env")

        try:
          with open('../botitoo/config.json') as f:
            self.config = json.load(f)
        except FileNotFoundError:
          print("Error: config.json not found. Please create it from config.json.template.")
          exit()

        self.db_params= {
            "host": self.env['DB_HOST'],
            "user": self.env['DB_USER'],
            "password": self.env['DB_PASS'],
            "dbname": self.env['DB_DATA']
        }
        self.db=psycopg.connect(**self.db_params)
        self.cursor = self.db.cursor()

        self.colors = [int(id) for id in self.config.get("colors")] # usually "colors" is an array, might mess up if it's not an array
        self.guildID = int(self.config.get("guildID"))
        self.general_chatID = int(self.config.get("general_chatID"))
        self.shoutout_channelID = int(self.config.get("shoutout_channelID"))
        self.count_channelID = int(self.config.get("count_channelID"))
        self.custom_role_subscriberID = int(self.config.get("custom_role_subscriberID"))
        self.server_log_channelID = int(self.config.get("server_log_channelID"))
        self.booster_roleID = int(self.config.get("booster_roleID"))
        self.youtube_memberID = int(self.config.get("youtube_memberID"))

        self.usedLink = None

        super().__init__(intents=intents, command_prefix='b!')
    
    def addToStorage(self, name, item):
        self.cursor.execute(f"SELECT name FROM previous WHERE name = '{name}'")
        result = self.cursor.fetchone()
        if result:
          self.cursor.execute(f"UPDATE previous SET storage = '{item}' WHERE name = '{name}'")
        else:
          self.cursor.execute(f"INSERT INTO previous (name, storage) VALUES ('{name}', '{item}')")
        self.db.commit()

    def deleteFromStorage(self, name): # add item??
      self.cursor.execute(f"DELETE FROM previous WHERE NAME = '{name}'")
      self.db.commit()

    def getStorage(self, name):
      self.cursor.execute(f"SELECT storage FROM previous WHERE name = '{name}'")  # apparently this isnt good but whatever. only thing that works
      result = self.cursor.fetchone()
      return result[0]

    async def on_connect(self):
        for filename in glob.iglob("botitoo/cogs/**", recursive=True):
            if filename.endswith(".py"):
                try:
                    file = os.path.basename(filename)
                    fn = filename.replace('/', '.').replace('\\', '.').replace(f'.{file}','')
                    cog = f"{fn}.{file.replace('.py', '')}"
                    await self.load_extension(cog)
                except Exception as e:
                    print(f"Failed to load cog {cog}")
                    print(e.with_traceback(None))
        print("Loaded {} cogs".format(len(self.cogs)))
        print('Logged in as {0.user}'.format(self))
       
    async def on_ready(self):
        try:
          synced = await self.tree.sync()
          print(f"Synced {len(synced)} commands")
        except Exception as e:
          print(e)
        
        await self.get_channel(1321148137494020157).send(":white_check_mark: **Bot is online!**")