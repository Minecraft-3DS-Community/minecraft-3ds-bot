# TODO: Now that cogs are set up, move to py-cord instead of discord.py

import discord
from discord.ext import commands
import os
import dotenv
import asyncio
import help

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD = int(os.getenv("GUILD"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents, case_insensitive=True)

bot.help_command = help.CustomHelp()
bot.get_cog = help.get_cog_case_insensitive.__get__(bot)

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
    print("Connected!")

asyncio.run(load_cogs())
bot.run(TOKEN)