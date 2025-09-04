import discord
from discord.ext import commands
import json

# load git_repos from a .json instead
with open("data/repos.json", "r", encoding="utf-8") as f:
    git_repos = json.load(f)

class MC3DS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repo', help="Returns the queried repo's link or a list of available repos if none is specified.")
    async def repo(self, ctx, repo_name: str):
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

    @commands.command(name='unistore', help="Info and instructions on installing the Minecraft 3DS Unistore.")
    async def unistore(self, ctx):
        embed = discord.Embed(
            title="Minecraft 3DS Unistore",
            description="The [Minecraft 3DS Unistore](https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore) is functionally an extension to Universal-Updater that allows you to download MC3DS mods directly from it.\n\nYou can install the Unistore by opening Universal-Updater, and going to Settings → Select Unistore → Add, and selecting the Minecraft 3DS Community Unistore in the list of recommended Unistores.",
            color=discord.Color.blue()
        )
        
        if ctx.message.reference:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await message.reply(embed=embed, mention_author=True)
        else:
             await ctx.send(embed=embed)

    @commands.command(name='cstick', help="Fix instructions for C-Stick issues caused by plugins.")
    async def cstick(self, ctx):
        embed = discord.Embed(
            title="C-Stick",
            description="Plugins such as the one included in the Megapack cause the C-Stick and other \"New 3DS\" buttons to not work.\n\n To fix this, open Rosalina menu, and go to Miscellaneous Options and enable Input Redirection.",
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Open Rosalina menu by pressing L + ↓ + Select.")
        
        if ctx.message.reference:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await message.reply(embed=embed, mention_author=True)
        else:
             await ctx.send(embed=embed)

    @commands.command(name='titleid', help="List of MC3DS' TitleIDs.")
    async def titleid(self, ctx):
        embed = discord.Embed(
            title="MC3DS TitleIDs",
            description="USA - `00040000001B8700`\nEUR - `000400000017CA00`\nJPN - `000400000017FD00`",
            color=discord.Color.blue(),
        )        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MC3DS(bot))