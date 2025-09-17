import discord
from discord.ext import commands
import random
import json
from datetime import datetime, timedelta
import os

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_xp_time = {}
        self.data_file = "./data/volatile/levels.json"
        self.user_data = {}
        self.bots_channel_id = 821305236467220490
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)

        with open(self.data_file, "r") as f:
            raw_data = json.load(f)
            self.user_data = raw_data

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.user_data, f, indent=2)


    def get_user_entry(self, user_id):
        return self.user_data.get(user_id)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        bots_channel = self.bot.get_channel(self.bots_channel_id)
        user_id = str(ctx.author.id)
        now = datetime.now()
        last_time = self.last_xp_time.get(user_id)

        if not last_time or now - last_time >= timedelta(minutes=1):
            xp_gain = random.randint(15, 25)
            self.last_xp_time[user_id] = now
            if self.get_user_entry(user_id)['level'] >= 5:
                # add "Level 5+" role to user if they dont have it
                member = await bots_channel.guild.fetch_member(user_id)
                role = discord.utils.get(bots_channel.guild.roles, name="Level 5+")
                if  role not in member.roles:
                    await member.add_roles(role)
                    print(f"Added Level 5+ role to {member.name}")
                    
            if self.add_xp(user_id, xp_gain):
                await bots_channel.send(f"Congratulations <@{user_id}>, you are now at level {self.get_user_entry(user_id)['level']}!")
    def add_xp(self, user_id, xp_gain):
        leveled_up = None
        user = self.get_user_entry(user_id)

        if not user:
            user = {
                "id": user_id,
                "xp": {
                    "userXp": 0,
                    "levelXp": 100,
                    "totalXp": 0
                },
                "level": 1
            }
            self.user_data[user_id] = user

        user["xp"]["userXp"] += xp_gain
        user["xp"]["totalXp"] += xp_gain

        if user["xp"]["userXp"] >= user["xp"]["levelXp"]:
            user["xp"]["userXp"] -= user["xp"]["levelXp"]
            user["level"] += 1
            new_level = user["level"]
            user["xp"]["levelXp"] = 5 * (new_level ** 2) + (50 * new_level) + 100
            print(f"{user_id} leveled up to {new_level}!")
            leveled_up = True

        self.save_data()
        return leveled_up
    
async def setup(bot):
    await bot.add_cog(Levels(bot))