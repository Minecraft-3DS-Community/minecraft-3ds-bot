import discord

from discord.ext import commands
from discord import app_commands

TOKEN = "token"
GUILD = "guild id"
ADMIN_ID = 968672493185413171

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

git_repos = {
    "shader": "https://github.com/ENDERMANYK/Minecraft-3ds-shader",
    "mobvariations": "https://github.com/pizza-beep/MC3DS-mob-variations",
    "mpseedpicker": "https://github.com/pizza-beep/MegaPack-seed-picker",
    "mppluginalt": "https://github.com/pizza-beep/Megapack-plugin-alternative",
    "3dstconverter": "https://github.com/pizza-beep/GUI-3dst-Converter",
    "scriptingplugin": "https://github.com/STBrian/MC3DS-Scripting-plugin",
    "mpplugin": "https://github.com/Cracko298/megapackPlugin",
    "banna" : "https://github.com/Cracko298/Banna",
    "ironbrute": "https://github.com/Cracko298/MC3DS-IronBrute",
    "mc3dsdecomp": "https://github.com/Cracko298/mc3ds-decomp",
    "animationsuite": "https://github.com/Cracko298/MC3DS-AnimationSuite",
    "modeleditor": "https://github.com/Cracko298/MC3DS-Model-Editor",
    "catool": "https://github.com/Cracko298/CombinedAudioTool",
    "worldmanager": "https://github.com/Cracko298/MC3DS-WorldManager",
    "rtxshader": "https://github.com/Cracko298/Minecraft3DS-RTX-Shader",
    "luma": "https://github.com/LumaTeam/Luma3DS?tab=readme-ov-file#installation-and-upgrade",
    "megapack": "https://github.com/wyndchyme/mc3ds-modern",
    "unistore": "https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore",
    "ipspatchtool": "https://github.com/Minecraft-3DS-Community/IPS-Patch-Tool",
    "wiki": "https://github.com/Minecraft-3DS-Community/Minecraft3DS-Wiki",
    "website": "https://github.com/Minecraft-3DS-Community/Minecraft-3DS-Community.github.io",
    "bot": "https://github.com/TheProgrammer1337/minecraft-3ds-bot",
    "stbunistore": "https://github.com/STBrian/stb-mc3ds-unistore",
    "texturemaker": "https://github.com/STBrian/mc3ds-texture-maker",
    "py3dst": "https://github.com/STBrian/py3dst",
    "blangeditor": "https://github.com/STBrian/MC3DS-Blang-Editor",
}

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD))
    await bot.change_presence(activity=discord.Game(name="Minecraft: New Nintendo 3DS Edition"))
    # remove default discord slop
    bot.remove_command("help")
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

@bot.command(name='repo')
async def repo(ctx, repo_name: str = None):
    if not repo_name:
        embed = discord.Embed(
            title="Repositories",
            description="Use `!repo <name>` to get a link.\n\n" + "\n".join(f"**{name}**" for name in sorted(git_repos.keys())),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return

    url = git_repos.get(repo_name.lower())
    if url:
        await ctx.send(url)
    else:
        await ctx.send(f"\"{repo_name}\" not found.")

@bot.command(name='online')
async def online(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/821470210992504832/1005981335208345671/IMG_2959.png")

@bot.command(name='megapackdocs')
async def megapackdocs(ctx):
    await ctx.send("https://wyndchyme.github.io/mc3ds-modern/")

@bot.command(name='website')
async def website(ctx):
    await ctx.send("https://www.minecraft3ds.org/")


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

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency * 1000, 1)))

bot.run(TOKEN)
