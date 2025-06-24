# TODO: Now that cogs are set up, move to py-cord instead of discord.py

import discord
from discord.ext import commands
import os
import dotenv
import asyncio

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD = int(os.getenv("GUILD"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

bot.GUILD = GUILD
bot.ADMIN_ID = ADMIN_ID

async def load_cogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD))
    await bot.change_presence(activity=discord.Game(name="Minecraft: New Nintendo 3DS Edition")) # :absoluteconclave:
    
    # remove default discord help command
    bot.remove_command("help")
    print("Connected!")

asyncio.run(load_cogs())
bot.run(TOKEN)