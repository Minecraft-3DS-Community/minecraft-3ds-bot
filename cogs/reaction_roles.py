import discord
from discord.ext import commands
from discord import app_commands
import json
import os

CONFIG_PATH = 'data/volatile/reaction_roles.json'

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_data = self.load_config()
        self.bot.tree.add_command(self.setupreaction, guild=discord.Object(id=self.bot.GUILD))

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.reaction_data, f, indent=4)

    @app_commands.command(name="setupreaction", description="Set up reaction role for a message")
    @app_commands.describe(message_id="Message ID", emoji="Emoji", role="Role")
    @app_commands.checks.has_role('Staff Team')
    @app_commands.default_permissions(manage_roles=True)
    async def setupreaction(self, interaction: discord.Interaction, message_id: str, emoji: str, role: discord.Role):
        msg_id = str(message_id)
        emoji_obj = discord.PartialEmoji.from_str(emoji)
        emoji_id = str(emoji_obj.id) if emoji_obj.id else emoji_obj.name
        
        # add reaction to the message
        try:
            channel = interaction.channel
            message = await channel.fetch_message(int(message_id))
            await message.add_reaction(emoji)
        except Exception as e:
            await interaction.response.send_message(f"Failed to add reaction: {e}", ephemeral=True)
            return
        
        if msg_id not in self.reaction_data:
            self.reaction_data[msg_id] = {}

        self.reaction_data[msg_id][emoji_id] = role.id
        self.save_config()
        
        await interaction.response.send_message(
            "Reaction role set!", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg_id = str(payload.message_id)
        emoji_id = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name

        if msg_id in self.reaction_data and emoji_id in self.reaction_data[msg_id]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.reaction_data[msg_id][emoji_id])
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg_id = str(payload.message_id)
        emoji_id = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name

        if msg_id in self.reaction_data and emoji_id in self.reaction_data[msg_id]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.reaction_data[msg_id][emoji_id])
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
