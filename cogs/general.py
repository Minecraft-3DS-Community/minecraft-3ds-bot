import discord
from discord.ext import commands
import json

# load git_repos from a .json instead
with open("data/repos.json", "r", encoding="utf-8") as f:
    git_repos = json.load(f)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repo')
    async def repo(self, ctx, repo_name: str = None):
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

    @commands.command(name='unistore')
    async def unistore(self, ctx):
        embed = discord.Embed(
            title="Minecraft 3DS Unistore",
            description="The [Minecraft 3DS Unistore](https://github.com/Minecraft-3DS-Community/minecraft-3ds-unistore) is functionally an extension to Universal-Updater that allows you to download MC3DS mods directly from it.\n\nYou can install the Unistore by opening Universal-Updater, and going to Settings → Select Unistore → Add, and selecting the Minecraft 3DS Community Unistore in the list of recommended Unistores.",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='cstick')
    async def cstick(self, ctx):
        embed = discord.Embed(
            title="C-Stick",
            description="Plugins such as the one included in the Megapack cause the C-Stick and other \"New 3DS\" buttons to not work.\n\n To fix this, open Rosalina menu, and go to Miscellaneous Options and enable Input Redirection.",
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Open Rosalina menu by pressing L + ↓ + Select.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))