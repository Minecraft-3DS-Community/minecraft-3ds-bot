import discord

from discord.ext import commands
from discord import app_commands

TOKEN = "token"
GUILD = "guild id"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD))
    await bot.change_presence(activity=discord.Game(name="Minecraft: New Nintendo 3DS Edition"))
    print("Connected!")

@bot.tree.command(
    name="terminate",
    description="Shuts down the bot",
    guild=discord.Object(id=GUILD)
)
async def terminate(interaction):
    if interaction.user.id == 968672493185413171:
        await interaction.response.send_message("Goodbye.", ephemeral=True)
        await bot.close()
    else:
        await interaction.response.send_message("No.", ephemeral=True)


@bot.command(name='online')
async def online(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/821470210992504832/1005981335208345671/IMG_2959.png")

@bot.command(name='megapackdocs')
async def online(ctx):
    await ctx.send("https://wyndchyme.github.io/mc3ds-modern/")

@bot.command(name='megapack')
async def megapack(ctx):
    await ctx.send("https://github.com/wyndchyme/mc3ds-modern")

@bot.command(name='website')
async def megapack(ctx):
    await ctx.send("https://www.minecraft3ds.org/")

@bot.command(name='unistore')
async def unistore(ctx):
    embed = discord.Embed(
        title="Minecraft 3DS Unistore",
        description="The [Minecraft 3DS Unistore](https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore) is functionally an extension to Universal-Updater that allows you to download MC3DS mods directly from it.\n\nYou can install the Unistore by opening Universal-Updater, and going to Settings → Select Unistore → Add, and selecting the Minecraft 3DS Community Unistore in the list of recommended Unistores.",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
