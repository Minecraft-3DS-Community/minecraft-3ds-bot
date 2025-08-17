import discord
from discord.ext import commands
from discord import app_commands
import os

# im too lazy to properly define this so whatever
GUH_ID = 1325357955016818688

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.terminate, guild=discord.Object(id=self.bot.GUILD))
    
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
