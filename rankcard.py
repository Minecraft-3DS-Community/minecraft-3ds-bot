from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_rank_card(username, level, current_xp, required_xp, ranknum, avatar_url):
    width, height = 925, 250

    def get_background_texture(level):
        if 0 <= level <= 4:
            return "dirt.png"
        elif 5 <= level <= 9:
            return "wood.png"
        elif 10 <= level <= 19:
            return "copper.png"
        elif 20 <= level <= 29:
            return "iron.png"
        elif 30 <= level <= 39:
            return "gold.png"
        elif 40 <= level <= 49:
            return "diamond.png"
        elif 50 <= level <= 59:
            return "emerald.png"
        elif 60 <= level:
            return "netherite.png"

    def draw_text_shadow(draw, position, text, font=None, fill=(0, 0, 0, 0)):
        if font is None:
            font = ImageFont.truetype("data/fonts/mojang-regular.ttf", 38)
        x, y = position
        draw.text((x + 5, y + 5), text, font=font, fill=(20, 20, 20, 255))
        draw.text((x, y), text, font=font, fill=fill)

    # background setup
    tile_path = get_background_texture(level)
    tile = Image.open(f"./data/blocks/{tile_path}").convert("RGBA")
    tile = tile.resize((tile.width * 10, tile.height * 10), Image.NEAREST)
    background = Image.new("RGBA", (width, height))
    for x in range(0, width, tile.width):
        for y in range(0, height, tile.height):
            background.paste(tile, (x, y))
    dark_overlay = Image.new("RGBA", (width, height), (20, 20, 20, 255))
    background = Image.blend(background, dark_overlay, alpha=0.45)

    card = background.copy()
    draw = ImageDraw.Draw(card)

    # avatar setup
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA").resize((150, 150), Image.LANCZOS)
    item_frame = Image.open("./data/blocks/item_frame.png").convert("RGBA").resize((200, 200), Image.LANCZOS)

    mask_size = (150 * 3, 150 * 3)
    mask = Image.new("L", mask_size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + mask_size, fill=255)
    mask = mask.resize((150, 150), Image.LANCZOS)
    avatar.putalpha(mask)

    outline_size = 155
    hi_res = outline_size * 3
    mask = Image.new("L", (hi_res, hi_res), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, hi_res, hi_res), fill=255)
    mask = mask.resize((outline_size, outline_size), Image.LANCZOS)
    circle = Image.new("RGBA", (outline_size, outline_size), (0, 0, 0, 255))
    circle.putalpha(mask)

    card.paste(item_frame, (25, 25), item_frame)
    card.paste(circle, (48, 48), circle)
    card.paste(avatar, (50, 50), avatar)

    # text & xp bar
    font = ImageFont.truetype("data/fonts/mojang-regular.ttf", 38)
    little_font = ImageFont.truetype("data/fonts/mojang-regular.ttf", 33)

    draw_text_shadow(draw, (255, 45), username, font=font, fill=(255, 255, 255))
    draw_text_shadow(draw, (255, 105), f"Level:  {level}", font=font, fill=(255, 255, 255))
    draw_text_shadow(draw, (255, 165), f"XP: {current_xp} / {required_xp}", font=font, fill=(255, 255, 255))

    bar_x, bar_y = 250, 210
    bar_width, bar_height = 500, 20
    xp_ratio = current_xp / required_xp
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], fill=(50, 50, 50))
    draw.rectangle([bar_x, bar_y, bar_x + int(bar_width * xp_ratio), bar_y + bar_height], fill=(0, 255, 0))

    rank_text = f"Rank:  #{ranknum}"
    bbox = draw.textbbox((0, 0), rank_text, font=little_font)
    text_width = bbox[2] - bbox[0]
    rank_position = (width - text_width - 20, 20)
    draw_text_shadow(draw, rank_position, rank_text, font=little_font, fill=(255, 255, 255))

    # save file to bytesio
    output = BytesIO()
    card.save(output, format="WEBP", lossless=True)
    output.seek(0)
    return output
