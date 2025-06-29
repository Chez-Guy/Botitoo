import os
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, date
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

        self.db_params= {
            "host": self.env['DB_HOST'],
            "user": self.env['DB_USER'],
            "password": self.env['DB_PASS'],
            "dbname": self.env['DB_DATA']
        }
        self.db=psycopg.connect(**self.db_params)
        self.cursor = self.db.cursor()

        """ 
        Change the variables below to configure with your own server
        A lot of these are based around roles created for channel members, discord subscribers, and other stuff,
        but can be replicated into your own server by changing these IDs to your own roles/channels
        """

        self.colors = [1193322620779778146,1193322880331690024,1193322903173857321,1193322915345731604,1193322927375003708,1193322940603838525,1199434340770267257,1204570321433272320] 
    
        self.guildID = 1128048701387055209

        self.general_chatID = 1128048705363251265

        self.shoutout_channelID = 1194447194137297129

        self.count_channelID = 1136238325825536070

        self.custom_role_subscriberID = 1345992570601209890

        self.server_log_channelID = 1321148137494020157

        self.booster_roleID = 1141138598880620627

        self.youtube_memberID = 1138520134118559884

        self.usedLink = None

        super().__init__(intents=intents, command_prefix='b!')

    '''
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
'''
    
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
    # (media share)


    # TODO: add other stuff from old botitoo file


    # end of custom functions
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