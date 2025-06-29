# Botitoo, the Discord Bot 🤖
Botitoo is a Discord bot built on [Discord.py](https://github.com/Rapptz/discord.py) and uses a [PostgreSQL](https://www.postgresql.org/) database. This bot is intended for use in the [Chezito's Cavern](https://discord.gg/chez) Discord server.

I've provided the packages this bot requires in the [requirements.txt](https://github.com/Chez-Guy/Botitoo/blob/main/requirements.txt) as well as the database template in [db_structure.sql](https://github.com/Chez-Guy/Botitoo/blob/main/db_structure.sql). Not *entirely* sure if the `db_structures.sql` will work when trying to import into a PostgreSQL database, but the structure and everything you'll need to set it up is in there, so you can look at it for reference. 🙂 If you do decide to pull the source code and put it in your own server, all of the variables that need to be changed for your own server are on lines 37 thru 51 in the main file [bot.py](https://github.com/Chez-Guy/Botitoo/blob/main/botitoo/bot.py).

As always, if any issues arrise using it in your own server, please post them in the [Issues](https://github.com/Chez-Guy/Botitoo/issues) tab, and I'll do my best to get on it!

## Features
### Commands:
- `/ping` - Simple ping command that is purely for testing whether or not the bot is working, and not the actual ping of the bot lol
- `/gif (name)` - List of GIFs picked out by the community and moderators for the bot to send (because people can't just send the GIFs themselve I guess, don't ask Chez why they wanted this command added, cause he doesn't know)
- `/get_count` - See what the current count is in the VIP-only counting channel
- `/set_count` - For mods to set the count of the VIP-only counting channel in case the bot goes offline and/or is inaccurate
- `/register_role` - For mods to link custom role subscribers to their custom role, so when they unsubscribe, their role will be revoked
