# Botitoo, the Discord Bot 🤖
Botitoo is a Discord bot built on [Discord.py](https://github.com/Rapptz/discord.py) and uses a [PostgreSQL](https://www.postgresql.org/) database. This bot is intended for use in the [Chezito's Cavern](https://discord.gg/chez) Discord server.

This is my first time making a project of mine open source and giving others the ability to clone it to their own instance, so if any issues arrise using it in your own server, please post them in the [Issues](https://github.com/Chez-Guy/Botitoo/issues) tab, and I'll do my best to get on it!

## Features
### Commands:
- `/ping` - Simple ping command that is purely for testing whether or not the bot is working, and not the actual ping of the bot lol
- `/gif (name)` - List of GIFs picked out by the community and moderators for the bot to send (because people can't just send the GIFs themselve I guess, don't ask Chez why they wanted this command added, cause he doesn't know)
- `/get_count` - See what the current count is in the VIP-only counting channel
- `/set_count` - For mods to set the count of the VIP-only counting channel in case the bot goes offline and/or is inaccurate
- `/register_role` - For mods to link custom role subscribers to their custom role, so when they unsubscribe, their role will be revoked

## Instructions
* Download [Python 3.11.12](https://www.python.org/downloads/release/python-31112/)
* Change to `botitoo/` directory 
* Create a Virtual Environment
```python -m venv .venv```
* Activate Virutal Environment
> * **For Windows (Command Prompt or PowerShell):**
> ```.venv\Scripts\activate```
> * **For macOS / Linux:**
> ```source .venv/bin/activate```
* Install packages 
```pip install -r requirements.txt```
* Create an `.env` file and add your Discord bot `TOKEN`, your PostgreSQL `DB_HOST`, `DB_USER`, `DB_PASS`, and `DB_DATA` 
* Rename `config.json.template` to `config.json` and fill in your server-specific IDs
* Start the bot
> * **For process manager ([PM2](https://pm2.keymetrics.io/)):**
> ```pm2 start botitoo-pm2.json```
> * **Python:**
> ```python main.py```

Database template is located in [db_structure.sql](https://github.com/Chez-Guy/Botitoo/blob/main/templates/db_structure.sql). Not *entirely* sure if the `db_structures.sql` will work if you try to import into a PostgreSQL database editor, but the structure and everything you'll need to set it up is in that file, so you can look at it for reference and try to copy it as best you can. 🙂 I'm sure any version PostgreSQL will work just fine.