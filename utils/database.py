from motor.motor_asyncio import AsyncIOMotorClient

import config


class DataBase:

    def __init__(self):
        self.cluster = AsyncIOMotorClient(config.MONGODB_LINK)
        self.users = self.cluster.ecodb.users

    async def get_data(self, member):
        return await self.users.find_one({"member_id": member.id, "guild_id": member.guild.id})

    async def insert_new_member(self, member):
        if await self.users.count_documents({"member_id": member.id, "guild_id": member.guild.id}) == 0:
            await self.users.insert_one(
                {
                    "member_id": member.id,
                    "guild_id": member.guild.id,
                    "balance": 300,
                    "xp": 0,
                    "lvl": 1
                }
            )

    async def update_member(self, member, values: dict):
        await self.users.update_one({"member_id": member.id,"guild_id": member.guild.id}, values)
