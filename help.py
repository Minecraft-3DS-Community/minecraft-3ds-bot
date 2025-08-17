import discord
from discord.ext import commands
import os
import dotenv
import asyncio

class CustomHelp(commands.HelpCommand):
    EXCLUDED_COMMANDS = {"help"}

    async def send_bot_help(self, mapping):
        destination = self.get_destination()
        embed = discord.Embed(
            title="Help Categories",
            description="Use `-help <category>` to see commands in a category.",
            color=discord.Color.blue()
        )
        for cog, commands_list in mapping.items():
            filtered = [
                cmd for cmd in commands_list
                if not cmd.hidden and cmd.name not in self.EXCLUDED_COMMANDS
            ]
            if filtered:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(
                    name=f"{cog_name}",
                    value=f"",
                    inline=True
                )
        await destination.send(embed=embed)

    async def send_cog_help(self, cog):
        destination = self.get_destination()
        embed = discord.Embed(
            title=f"{cog.qualified_name} (1/1)",
            color=discord.Color.blue()
        )
        filtered = [
            cmd for cmd in cog.get_commands()
            if (
                not cmd.hidden and
                (cmd.short_doc or cmd.help)
            )
        ]
        for cmd in filtered:
            params = [
                f"[{name}]" for name, param in cmd.clean_params.items()
            ]
            param_str = " " + " ".join(params) if params else ""
            embed.add_field(
                name=f"-{cmd.name}{param_str}",
                value=cmd.short_doc or cmd.help,
                inline=False
            )
        await destination.send(embed=embed)
        
    def command_not_found(self, string: str, /) -> str:
        return f"No category called `{string}` found."

    maybe_coro = discord.utils.maybe_coroutine

    # disable command
    async def send_command_help(self, command):
        destination = self.get_destination()
        await destination.send(f"No category called `{command.name}` found.")

    # disable command
    async def send_group_help(self, group):
        destination = self.get_destination()
        await destination.send(f"No category called `{group.name}` found.")
        
def get_cog_case_insensitive(self, name):
        name = name.lower()
        for cog in self.cogs.values():
            if cog.qualified_name.lower() == name:
                return cog
        return None
