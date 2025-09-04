import discord
from discord.ext import commands
from discord import app_commands
import os
from rankcard import generate_rank_card
import time

# im too lazy to properly define this so whatever
GUH_ID = 1325357955016818688

class Misc(commands.Cog):
    rankcard_cooldowns = {}
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.terminate, guild=discord.Object(id=self.bot.GUILD))

    @commands.command(name='rank', help="Displays the user's rank card.")
    async def rank(self, ctx):
        
        author_id = str(ctx.author.id)
        now = time.time()
        last_used = self.rankcard_cooldowns.get(author_id, 0)
        if now - last_used < 10:
            await ctx.send(f"Please wait {int(10 - (now - last_used))} seconds before using this command again.")
            return
        self.rankcard_cooldowns[author_id] = now
        
        # weird cog import thing
        levels_cog = self.bot.get_cog("Levels")

        # get user
        target = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
        user_id = str(target.id)
        user_entry = levels_cog.get_user_entry(user_id)
        if not user_entry:
            return

        username = target.global_name
        level = user_entry["level"]
        current_xp = user_entry["xp"]["userXp"]
        required_xp = user_entry["xp"]["levelXp"]
        all_users = list(levels_cog.user_data.values())
        sorted_users = sorted(all_users, key=lambda u: u["xp"]["totalXp"], reverse=True)
        ranknum = next((i+1 for i, u in enumerate(sorted_users) if u["id"] == user_id), None)
        avatar_url = target.display_avatar.url

        card_bytes = generate_rank_card(username, level, current_xp, required_xp, ranknum, avatar_url)
        file = discord.File(card_bytes, filename="rankcard.webp")
        await ctx.send(file=file)

    @commands.command(name='online')
    async def online(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/821470210992504832/1005981335208345671/IMG_2959.png")

    @commands.command(name='website', help="Official Minecraft 3DS Community website link.")
    async def website(self, ctx):
        await ctx.send("https://www.minecraft3ds.org/")

    @commands.command(name='ping', help="Checks MC3DS Bot's latency in ms.")
    async def ping(self, ctx):
        await ctx.send('Pong! {0}ms'.format(round(self.bot.latency * 1000, 1)))
        
    @commands.command(name='pong')
    async def pong(self, ctx):
        await ctx.send('Ping!')

    @commands.command(name='guh', help=":guh:")
    async def guh(self, ctx):
        GUH = self.bot.get_emoji(GUH_ID)
        await ctx.message.add_reaction(GUH)
    
    # command tree commands

    @app_commands.command(
        name="terminate",
        description="Shuts down the bot",
    )
    async def terminate(self, interaction: discord.Interaction):
        if interaction.user.id == self.bot.ADMIN_ID:
            await interaction.response.send_message("Goodbye.", ephemeral=True)
            await self.bot.close()
        else:
            await interaction.response.send_message("No.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Misc(bot))
