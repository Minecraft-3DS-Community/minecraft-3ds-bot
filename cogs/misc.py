import discord
from discord.ext import commands
from discord import app_commands
import os

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.terminate, guild=discord.Object(id=self.bot.GUILD))
        self.bot.tree.add_command(self.sync, guild=discord.Object(id=self.bot.GUILD))
    
    @commands.command(name='online')
    async def online(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/821470210992504832/1005981335208345671/IMG_2959.png")

    @commands.command(name='website')
    async def website(self, ctx):
        await ctx.send("https://www.minecraft3ds.org/")
        
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong! {0}ms'.format(round(self.bot.latency * 1000, 1)))

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
            
    @app_commands.command(
        name="sync",
        description="Syncs the command tree",
    )
    async def sync(self, interaction: discord.Interaction):
        if interaction.user.id == self.bot.ADMIN_ID:
            await interaction.response.send_message("Syncing...", ephemeral=True)
            await self.bot.tree.sync()
        else:
            await interaction.response.send_message("No.", ephemeral=True)

    

async def setup(bot):
    await bot.add_cog(Misc(bot))