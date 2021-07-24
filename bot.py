import discord
from discord.ext import commands
from pymongo import MongoClient
import os

client = commands.Bot(command_prefix = "!", intents = discord.Intents(messages = True, guild_messages = True, members = True, guilds = True))
cluster = MongoClient("link")
collection = cluster.ecodb.colldb


@client.event
async def on_ready():
	print("Bot connected to the server")

	for guild in client.guilds:
		for member in guild.members:
			post = {
				"_id": member.id,
				"guild_id": guild.id,
				"balance": 300,
				"xp": 0,
				"lvl": 1
			}

			if collection.count_documents({"_id": member.id}) == 0:
				collection.insert_one(post)


@client.event
async def on_member_join(member):
	post = {
		"_id": member.id,
		"guild_id": guild.id,
		"balance": 300,
		"xp": 0,
		"lvl": 1
	}

	if collection.count_documents({"_id": member.id}) == 0:
		collection.insert_one(post)


@client.event
async def on_command_error(ctx, error):
	print(error)

	if isinstance(error, commands.UserInputError):
		await ctx.send(embed = discord.Embed(
			description = f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`"
		))


@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	client.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run("token")