import disnake
from disnake.ext import commands

from motor.motor_asyncio import AsyncIOMotorClient


class ServerEvents(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		self.cluster = AsyncIOMotorClient("LINK")
		self.coll = self.cluster.DATABASE_NAME.COLLECTION_NAME

	@commands.Cog.listener()
	async def on_ready():
		for guild in bot.guilds:
			if await self.coll.count_documents({"member_id": member.id}) == 0:
				await self.coll.insert_one(
					{
						"member_id": member.id,
						"guild_id": guild.id,
						"balance": 300,
						"xp": 0,
						"lvl": 1
					}
				)

	@commands.Cog.listener()
	async def on_message(message):
		if message.author == self.bot.user:
			return

		data = await self.coll.find_one({"member_id": message.author.id, "guild_id": message.guild.id})
		if data["xp"] == 500+100 * data["lvl"]:
			await self.coll.update_one(
				{
					"member_id": message.author.id,
					"guild_id": message.guild.id
				},
				{
					"$set": {
						"lvl": data["lvl"] + 1,
						"xp": 0
					}
				}
			)

			await message.channel.send(f"{message.author.mention} +1 LVL")
		else:
			await self.coll.update_one(
				{
					"member_id": message.author.id,
					"guild_id": message.guild.id
				},
				{
					"$set": {
						"xp": data["xp"] + 50
					}
				}
			)

	@commands.Cog.listener()
	async def on_member_join(member):
		if await self.coll.count_documents({"member_id": member.id}) == 0:
			await self.coll.insert_one(
				{
					"member_id": member.id,
					"guild_id": member.guild.id,
					"balance": 300,
					"xp": 0,
					"lvl": 1
				}
			)

	@commands.Cog.listener()
	async def on_command_error(ctx, error):
		print(error)

		if isinstance(error, commands.UserInputError):
			await ctx.send(embed=disnake.Embed(
				description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`"
			))


def setup(bot):
	bot.add_cog(ServerEvents(bot))
