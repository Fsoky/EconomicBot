import os

import disnake
from disnake.ext import commands

import config

bot = commands.Bot(command_prefix="!", intents=disnake.Intents(messages=True, guild_messages=True, members=True, guilds=True))


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
	bot.load_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
	bot.reload_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
	bot.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.TOKEN)
