import discord
from PIL import Image
from discord.ext import commands
from discord import app_commands, File
from discord import File
from py3dst import Texture3dst
from io import BytesIO
import tempfile
import os
import dotenv


dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD = int(os.getenv("GUILD"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)
git_repos = {
    "shader": "https://github.com/ENDERMANYK/Minecraft-3ds-shader",
    "felsker": "https://github.com/pizza-beep/Felsker",
    "mpplugin": "https://github.com/Cracko298/megapackPlugin",
    "ironbrute": "https://github.com/Cracko298/MC3DS-IronBrute",
    "mc3dsdecomp": "https://github.com/Cracko298/mc3ds-decomp",
    "animationsuite": "https://github.com/Cracko298/MC3DS-AnimationSuite",
    "modeleditor": "https://github.com/Cracko298/MC3DS-Model-Editor",
    "catool": "https://github.com/Cracko298/CombinedAudioTool",
    "worldmanager": "https://github.com/Cracko298/MC3DS-WorldManager",
    "rtxshader": "https://github.com/Cracko298/Minecraft3DS-RTX-Shader",
    "luma": "https://github.com/LumaTeam/Luma3DS?tab=readme-ov-file#installation-and-upgrade",
    "3dschunker": "https://github.com/MC3DS-Save-Research/3DS-Chunker",
    "unistore": "https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore",
    "ipspatchtool": "https://github.com/Minecraft-3DS-Community/IPS-Patch-Tool",
    "website": "https://github.com/Minecraft-3DS-Community/Minecraft-3DS-Community.github.io",
    "mobvariations": "https://github.com/pizza-beep/MC3DS-mob-variations",
    "mpseedpicker": "https://github.com/pizza-beep/MegaPack-seed-picker",
    "mppluginalt": "https://github.com/pizza-beep/Megapack-plugin-alternative",
    "3dstconverter": "https://github.com/pizza-beep/GUI-3dst-Converter",
    "mc3dsgrimes": "https://github.com/sewene/mc3ds-grimes",
    "stbunistore": "https://github.com/STBrian/stb-mc3ds-unistore",
    "texturemaker": "https://github.com/STBrian/mc3ds-texture-maker",
    "py3dst": "https://github.com/STBrian/py3dst",
    "pybjson": "https://github.com/STBrian/pyBjson",
    "blangeditor": "https://github.com/STBrian/MC3DS-Blang-Editor",
    "bjsoneditor": "https://github.com/STBrian/MC3DS-BJSON-Editor",
    "lunacore": "https://github.com/STBrian/LunaCore",
    "bot": "https://github.com/TheProgrammer1337/minecraft-3ds-bot",
    "megapack": "https://github.com/wyndchyme/mc3ds-modern"
}

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD))
    await bot.change_presence(activity=discord.Game(name="Minecraft: New Nintendo 3DS Edition"))
    # remove default discord slop
    bot.remove_command("help")
    print("Connected!")

@bot.event
async def on_message(ctx):
    
    # auto convert *.bmp to *.png and send it
    png_files = []
    if ctx.attachments:
        for attachment in ctx.attachments:
            if attachment.filename.lower().endswith('.bmp'):
                try:
                    img_bytes = await attachment.read()
                    bmp_buffer = BytesIO(img_bytes)
                    img = Image.open(bmp_buffer)

                    png_buffer = BytesIO()
                    img.save(png_buffer, format="PNG")
                    png_buffer.seek(0)

                    png_files.append(
                        discord.File(
                            png_buffer,
                            filename=attachment.filename.rsplit('.', 1)[0] + ".png"
                        )
                    )
                except Exception as e:
                    await print(f"Failed to convert {attachment.filename} to PNG {e}")

        if png_files:
            await ctx.channel.send(files=png_files)

    await bot.process_commands(ctx)

@bot.command(name='repo')
async def repo(ctx, repo_name: str = None):
    if not repo_name:
        embed = discord.Embed(
            title="Available Repositories",
            description="Use `-repo <name>` to get a link.\n\n" + "\n".join(f"**{name}**" for name in sorted(git_repos.keys())),
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

@bot.tree.command(
    name="convertfrom3dst",
    description="Convert a *.3dst file to *.png",
    guild=discord.Object(id=GUILD)
)
async def reverse3dst(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer()
    if not file.filename.lower().endswith('.3dst'):
        await interaction.followup.send("Invalid file extension.", ephemeral=True)
        return
    filename = file.filename.removesuffix('.3dst')
    try:
        file_bytes = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".3dst", delete=False) as tmp:
            temp_path = tmp.name
            tmp.write(file_bytes)

        try:
            tex = Texture3dst().open(temp_path)
            
            image = tex.copy(0, 0, tex.size[0], tex.size[1])
            output = BytesIO()
            image.save(output, format="PNG")
            output.seek(0)
        finally:
            os.remove(temp_path)

        await interaction.followup.send(
            file=File(fp=output, filename=filename + ".png"),
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"Failed to convert 3dst: {e}")

@bot.tree.command(
    name="convertto3dst",
    description="Convert an image to *.3dst",
    guild=discord.Object(id=GUILD)
)
async def convert3dst(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer()
    if not file.filename.lower().endswith(('.png', '.bmp')):
        await interaction.followup.send("Invalid file extension")
        return
    filename = file.filename.rsplit('.', 1)[0]
    try:
            
        img_bytes = await file.read()
        img = Image.open(BytesIO(img_bytes)).convert("RGBA")
        tex = Texture3dst().fromImage(img)
        
        tex.export("temp.3dst")
        with open("temp.3dst", "rb") as f:
            image = BytesIO(f.read())
        
        image.seek(0)

        await interaction.followup.send(file=File(fp=image, filename=filename + ".3dst"))
        os.remove("temp.3dst")
    except Exception as e:
        print(f"Failed to convert image: {e}")

bot.run(TOKEN)
