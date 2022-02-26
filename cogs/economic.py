import disnake
from disnake.ext import commands

from motor.motor_asyncio import AsyncIOMotorClient


class Economic(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		self.cluster = AsyncIOMotorClient("LINK")
		self.coll = self.cluster.DATABASE_NAME.COLLECTION_NAME

	@commands.command(
		name="баланс",
		aliases=["cash"],
		brief="Вывод баланса пользователя",
		usage="balance <@user>"
	)
	async def balance(self, ctx, member: disnake.Member=None):
		values = {"member_id": ctx.author.id, "guild_id": ctx.guild.id}
		embed = disnake.Embed(
			description=f"Баланса пользователя __{ctx.author}__: **{await self.coll.find_one(values)}**"
		)

		if member is not None:
			values["member_id"] = member.id
			embed.description = f"Баланса пользователя __{ctx.author}__: **{await self.coll.find_one(values)}**"

		await ctx.send(embed=embed)

	@commands.command(
		name="перевод",
		aliases=["give-cash", "givecash"],
		brief="Перевод денег другому пользователю",
		usage="pay <@user> <amount>"
	)
	async def pay(self, ctx, member: disnake.Member, amount: int):
		values = {"member_id": ctx.author.id, "guild_id": ctx.guild.id}
		balance = await self.coll.find_one(values)["balance"]
		embed = disnake.Embed()

		if member.id == ctx.author.id:
			embed.description = f"__{ctx.author}__, конечно извините меня, но проход жучкам сегодня закрыт."

		if amount <= 0:
			embed.description = f"__{ctx.author}__, конечно извините меня, но проход жучкам сегодня закрыт."
		elif balance <= 0:
			embed.description = f"__{ctx.author}__, недостаточно средств"
		else:
			await self.coll.update_one(values, {"$inc": {"balance" -amount}})

			values["member_id"] = member.id
			await self.coll.update_one(values, {"$inc": "balance" +amount})

			embed.description = f"__{ctx.author}__, транзакция прошла успешно"

		await ctx.send(embed=embed, delete_after=5)


def setup(bot):
	bot.add_cog(Economic(bot))
