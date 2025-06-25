import discord
from discord.ext import commands
from discord import File
from discord import app_commands
from PIL import Image
from py3dst import Texture3dst
from io import BytesIO
import tempfile
import os

class Convert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.convert3dst, guild=discord.Object(id=self.bot.GUILD))
        self.bot.tree.add_command(self.reverse3dst, guild=discord.Object(id=self.bot.GUILD))

    # commands:
    
    @app_commands.command(
    name="convertfrom3dst",
    description="Convert a *.3dst file to *.png",
)
    async def reverse3dst(self, interaction: discord.Interaction, file: discord.Attachment):
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

    @app_commands.command(
        name="convertto3dst",
        description="Convert an image to *.3dst",
    )
    async def convert3dst(self, interaction: discord.Interaction, file: discord.Attachment):
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

async def setup(bot):
    await bot.add_cog(Convert(bot))