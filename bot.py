import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import asyncio

# --- CONFIG ---
API_ID = "21552265"
API_HASH = "1c971ae7e62cc416ca977e040e700d09"
BOT_TOKEN = "7664042669:AAEX4IU21H1r27Pu1kvDNiCowUg8F6t1-jM"

GROUP_LINK_1 = "https://t.me/+I-nuO3khvMUwZmY1"
GROUP_LINK_2 = "https://t.me/+I-nuO3khvMUwZmY1"
START_IMAGE_URL = "https://i.ibb.co/0jFF4gcX/IMG-20251002-065908-636.jpg"

# --- SEARCH SITES (YouTube removed) ---
SEARCH_SITES = [
    "xnxx.com",
    "xvideos.com",
    "xhamster.com",
    "pornhub.com",
    "porn.com",
    "fuq.com",
    "tube8.com",
    "youporn.com",
    "spankbang.com",
    "redtube.com"
]

# --- PORN CATEGORIES ---
PORN_CATEGORIES = [
    ("Deshi", "desi porn"),
    ("Indian", "indian porn"),
    ("Young", "young porn"),
    ("Wife", "indian wife porn"),
    ("College", "college porn"),
    ("Teen", "teen porn"),
    ("Lesbian", "lesbian porn"),
    ("Milf", "milf porn"),
    ("Anal", "anal porn"),
    ("HD", "hd porn"),
]

# --- FUNCTION TO GET VIDEO URL USING yt-dlp ---
def get_video_url(search_term):
    site = random.choice(SEARCH_SITES)
    query = f"ytsearch10:{search_term} site:{site}"  # fixed search syntax
    
    ydl_opts = {
        "format": "best[ext=mp4]",
        "noplaylist": True,
        "quiet": True,
        "default_search": "auto"
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info and info["entries"]:
                info = random.choice(info["entries"])
            return info.get("url")
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return None

# --- INIT BOT ---
app = Client("pornbot_categories", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- START COMMAND ---
@app.on_message(filters.command("start"))
async def porn_start(client, message):
    keyboard_buttons = []
    row = []
    for idx, (display, _) in enumerate(PORN_CATEGORIES):
        row.append(InlineKeyboardButton(display, callback_data=f"porn_{idx}"))
        if len(row) == 3:
            keyboard_buttons.append(row)
            row = []
    if row:
        keyboard_buttons.append(row)

    # Add group buttons at the top
    keyboard_buttons.insert(0, [InlineKeyboardButton("Join Group 1", url=GROUP_LINK_1)])
    keyboard_buttons.insert(1, [InlineKeyboardButton("Join Group 2", url=GROUP_LINK_2)])

    await message.reply_photo(
        START_IMAGE_URL,
        caption="Welcome to PornBot!\nJoin our groups and choose your favorite type below.",
        reply_markup=InlineKeyboardMarkup(keyboard_buttons)
    )

# --- CATEGORY BUTTON HANDLERS ---
for idx, (display, search_term) in enumerate(PORN_CATEGORIES):
    async def handler(client, query, search_term=search_term, display=display):
        await query.answer("Fetching video... please wait ⏳")
        video_url = await asyncio.to_thread(get_video_url, search_term)
        if video_url:
            try:
                await query.message.reply_video(video_url, caption=f"{display}")
            except Exception:
                # fallback if video too big
                await query.message.reply(f"Cannot send video, watch here: {video_url}")
        else:
            await query.message.reply(f"No video found for {display}.")
    app.on_callback_query(filters.regex(f"^porn_{idx}$"))(handler)

# --- RUN BOT ---
if __name__ == "__main__":
    app.run()
