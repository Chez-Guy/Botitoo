import os
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, date
from dotenv import dotenv_values
import glob
import requests
import mysql.connector
import json

class Botitoo(commands.Bot):
    def __init__(self):

        # define variables and stuff here (define with self.[name])

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.integrations = True
        intents.reactions = True
        
        self.env = dotenv_values(".env")

        self.db=mysql.connector.connect(
            host=self.env['DB_HOST'],
            user=self.env['DB_USER'],
            passwd=self.env['DB_PASS'],
            database=self.env['DB_DATA']
            )
        self.cursor = self.db.cursor(buffered=True)

        self.colors = [1193322620779778146,1193322880331690024,1193322903173857321,1193322915345731604,1193322927375003708,1193322940603838525,1199434340770267257,1204570321433272320] 
        # roles are in order with how they appear in discord. im sure it doesnt matter but whatever

        global usedLink
        self.usedLink = usedLink

        super().__init__(intents=intents, command_prefix='b!')


    # put functions here to be used elsewhere

    # media share
    def addToMediaShare(id):
        url = "https://api.streamelements.com/kappa/v2/songrequest/602b0c4de3c04194085015db/queue"

        payload = json.dumps({
          "video": id
        })
        headers = {
          'Accept': 'application/json; charset=utf-8, application/json',
          'Authorization': 'Bearer '+os.getenv('SE_TOKEN'),
          'Content-Type': 'application/json'
        }

        requests.request("POST", url, headers=headers, data=payload)

    def validLink(self, input): # input is whole message content
      links = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/watch?v=", "https://youtube.com/shorts/"] # get every possible link
      for link in links:
        if link in input:
          self.usedLink = link
          return True
      return False
    
    # submissions or media_share_users for database
    def changeMS_database(self, database, change, id, val=None): # id is user's id, val is how much to change by (default for val is none for funcs that want to read)
      self.cursor.execute('SELECT id FROM '+database+' WHERE id="'+str(id)+'"')
      if self.cursor.fetchone(): # check if usr exists in db
        if change=="read":
          self.cursor.execute('SELECT count FROM '+database+' WHERE id="'+str(id)+'"')
          return self.cursor.fetchone()[0]
        elif change=="write":
          self.cursor.execute('UPDATE '+database+' SET count = '+str(self.changeMS_database(database, "read", id)+val)+' WHERE id = "'+str(id)+'"')
          self.db.commit()
      else:
        self.cursor.execute('INSERT INTO '+database+' (id, count) VALUES ("'+str(id)+'", 0)')
        self.db.commit()
        return 1

    #TODO: make command in discord to whitelist video/user
    #TODO: update to check for roles to whitelist if its for users?
    def checkWhitelist(self, database, id):
      self.cursor.execute('SELECT whitelisted FROM '+database+' WHERE id="'+str(id)+'"')
      result = self.cursor.fetchone()
      if result:
        if result[0]==1: return True 
        elif result[0]==0: return False

    
    def addToStorage(self, name, item):
        self.cursor.execute('SELECT name FROM previous WHERE name = "'+name+'"')
        result = self.cursor.fetchone()
        if result:
          query = "UPDATE previous SET storage = %s WHERE name = %s"
          self.cursor.execute(query, (item, name))
        else:
          query = 'INSERT INTO previous (name, storage) VALUES (%s, %s)'
          self.cursor.execute(query, (name, item))
        self.db.commit()

    def deleteFromStorage(self, name): # add item??
      self.cursor.execute('DELETE FROM previous WHERE NAME = "'+name+'"')
      self.db.commit()

    def getStorage(self, name):
      self.cursor.execute('SELECT storage FROM previous WHERE name = "'+name+'"')  # apparently this isnt good but whatever. only thing that works
      result = self.cursor.fetchone()
      return result[0]
    # (media share)


    # TODO: add other stuff from old botitoo file


    # end of custom functions
    async def on_connect(self):
        for filename in glob.iglob("cogs/**", recursive=True):
            if filename.endswith(".py"):
                print(filename)
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
        await self.bot.get_channel(1321148137494020157).send(":white_check_mark: **Bot is online!**")
       
    async def on_ready(self):
        try:
          synced = await self.tree.sync()
          print(f"Synced {len(synced)} commands")
        except Exception as e:
          print(e)