import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO


GUH_ID = 1325357955016818688
JOIN_LEAVE_ID = 821298578713477142

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        # :guh: reaction
        GUH = self.bot.get_emoji(GUH_ID)
        if ctx.channel.id == JOIN_LEAVE_ID:
            await ctx.add_reaction(GUH)
            
            
        # handle bmp to png conversion
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
                await ctx.reply(files=png_files, mention_author=False)
                

        # await self.bot.process_commands(ctx)
        
        pass

async def setup(bot):
    await bot.add_cog(Events(bot))