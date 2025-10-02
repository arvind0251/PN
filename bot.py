import asyncio
import random
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = "21552265"
API_HASH = "1c971ae7e62cc416ca977e040e700d09"
BOT_TOKEN = "7664042669:AAEX4IU21H1r27Pu1kvDNiCowUg8F6t1-jM"

GROUP_LINK_1 = "https://t.me/+I-nuO3khvMUwZmY1"
GROUP_LINK_2 = "https://t.me/+I-nuO3khvMUwZmY1"
START_IMAGE_URL = "https://i.ibb.co/0jFF4gcX/IMG-20251002-065908-636.jpg"

# --- PORN CATEGORIES ---
PORN_CATEGORIES = [
    ("Deshi", "desi"),
    ("Indian", "indian"),
    ("Young", "young"),
    ("Wife", "wife"),
    ("College", "college"),
    ("Teen", "teen"),
    ("Lesbian", "lesbian"),
    ("Milf", "milf"),
    ("Anal", "anal"),
    ("HD Desi", "hd desi"),
]

# --- ADULT SITES TO SCRAPE ---
SEARCH_SITES = [
    "https://www.xnxx.com/search/{}",
    "https://www.xvideos.com/?k={}",
    "https://xhamster.com/search?q={}",
    "https://www.pornhub.com/video/search?search={}"
]

# --- FUNCTION TO SCRAPE VIDEO URL ---
def scrape_video(search_term):
    random.shuffle(SEARCH_SITES)  # random site order
    for site_template in SEARCH_SITES:
        url = site_template.format(search_term.replace(" ", "+"))
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Try to find video links
            links = []
            if "xnxx.com" in url:
                thumbs = soup.find_all("div", class_="thumb")
                for t in thumbs:
                    a_tag = t.find("a", href=True)
                    if a_tag:
                        links.append("https://www.xnxx.com" + a_tag["href"])
            elif "xvideos.com" in url:
                thumbs = soup.find_all("div", class_="thumb-block")
                for t in thumbs:
                    a_tag = t.find("a", href=True)
                    if a_tag:
                        links.append("https://www.xvideos.com" + a_tag["href"])
            elif "xhamster.com" in url:
                thumbs = soup.find_all("div", class_="video-thumb")
                for t in thumbs:
                    a_tag = t.find("a", href=True)
                    if a_tag:
                        links.append("https://xhamster.com" + a_tag["href"])
            elif "pornhub.com" in url:
                thumbs = soup.find_all("a", class_="js-pop videoblock")
                for t in thumbs:
                    href = t.get("href")
                    if href:
                        links.append("https://www.pornhub.com" + href)
            
            if links:
                return random.choice(links)
        except Exception as e:
            print(f"Scraping error ({url}): {e}")
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
        video_url = await asyncio.to_thread(scrape_video, search_term)
        if video_url:
            try:
                await query.message.reply_video(video_url, caption=f"{display}")
            except Exception:
                await query.message.reply(f"Cannot send video, watch here: {video_url}")
        else:
            await query.message.reply(f"No video found for {display}.")
    app.on_callback_query(filters.regex(f"^porn_{idx}$"))(handler)

# --- RUN BOT ---
if __name__ == "__main__":
    app.run()
