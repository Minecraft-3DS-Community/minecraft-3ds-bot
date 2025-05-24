import discord

from discord.ext import commands
from discord import app_commands

TOKEN = "token"
GUILD = "guild id"
ADMIN_ID = 968672493185413171

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
    if interaction.user.id == ADMIN_ID:
        await interaction.response.send_message("Goodbye.", ephemeral=True)
        await bot.close()
    else:
        await interaction.response.send_message("No.", ephemeral=True)
        
@bot.command(name='online')
async def online(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/821470210992504832/1005981335208345671/IMG_2959.png")

@bot.command(name='megapackdocs')
async def megapackdocs(ctx):
    await ctx.send("https://wyndchyme.github.io/mc3ds-modern/")

@bot.command(name='megapack')
async def megapack(ctx):
    await ctx.send("https://github.com/wyndchyme/mc3ds-modern")

@bot.command(name='website')
async def website(ctx):
    await ctx.send("https://www.minecraft3ds.org/")

@bot.command(name='texturemaker')
async def texturemaker(ctx):
    await ctx.send("https://github.com/STBrian/mc3ds-texture-maker")

@bot.command(name='unistore')
async def unistore(ctx):
    embed = discord.Embed(
        title="Minecraft 3DS Unistore",
        description="The [Minecraft 3DS Unistore](https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore) is functionally an extension to Universal-Updater that allows you to download MC3DS mods directly from it.\n\nYou can install the Unistore by opening Universal-Updater, and going to Settings → Select Unistore → Add, and selecting the Minecraft 3DS Community Unistore in the list of recommended Unistores.",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)

@bot.command(name='cstick')
async def cstick(ctx):
    embed = discord.Embed(
        title="C-Stick",
        description="Plugins such as the one included in the Megapack cause the C-Stick and other \"New 3DS\" buttons to not work.\n\n To fix this, open Rosalina menu, and go to Miscellaneous Options and enable Input Redirection.",
        color=discord.Color.blue(),
    )
    embed.set_footer(text="Open Rosalina menu by pressing L + ↓ + Select.")
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
