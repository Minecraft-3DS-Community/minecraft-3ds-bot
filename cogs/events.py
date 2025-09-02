import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from discord.utils import get

GUH_ID = 1325357955016818688
JOIN_LEAVE_ID = 821298578713477142
CLANKERBAIT_ID = 1327124480300154910

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        # :guh: reaction
        GUH = self.bot.get_emoji(GUH_ID)
        if ctx.channel.id == JOIN_LEAVE_ID:
            await ctx.add_reaction(GUH)
        
        # clankerbait 
        if ctx.channel.id == CLANKERBAIT_ID:
            role = get(ctx.author.roles, name='Staff Team')
            if role:
                return
            
            if ctx.author.id == self.bot.ADMIN_ID:
                return
                
            await ctx.author.kick(reason="Sent a message in #clanker-bait")
            await ctx.delete()
            print(f"Kicked {ctx.author} for sending a message in #clanker-bait")

        # handle bmp to webp conversion
        webp_files = []
        if ctx.attachments:
            for attachment in ctx.attachments:
                if attachment.filename.lower().endswith('.bmp'):
                    try:
                        img_bytes = await attachment.read()
                        bmp_buffer = BytesIO(img_bytes)
                        img = Image.open(bmp_buffer)

                        webp_buffer = BytesIO()
                        img.save(webp_buffer, format="WEBP", lossless=True)
                        webp_buffer.seek(0)

                        webp_files.append(
                            discord.File(
                                webp_buffer,
                                filename=attachment.filename.rsplit('.', 1)[0] + ".webp"
                            )
                        )
                    except Exception as e:
                        await print(f"Failed to convert {attachment.filename} to WEBP {e}")

            if webp_files:
                await ctx.reply(files=webp_files, mention_author=False)


        # await self.bot.process_commands(ctx)
        
        pass

async def setup(bot):
    await bot.add_cog(Events(bot))