import random
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

GROUP_LINK_1 = "https://t.me/yourgroup1"
GROUP_LINK_2 = "https://t.me/yourgroup2"
START_IMAGE_URL = "https://i.imgur.com/yourimage.jpg"  # Replace with your image

SEARCH_SITES = [
    "https://www.xnxx.com/search/{}",
    "https://www.xvideos.com/?k={}",
    "https://xhamster.com/search?q={}",
    "https://www.pornhub.com/video/search?search={}",
    "https://www.porn.com/search?q={}",
    "https://www.fuq.com/search?q={}",
    "https://www.tube8.com/search/videos/{}",
    "https://www.youporn.com/search/?query={}",
    "https://spankbang.com/s/{}",
    "https://www.redtube.com/?search={}"
]

# Define all porn categories and their display names here!
PORN_CATEGORIES = [
    ("Deshi", "desi porn"),
    ("Indian", "indian porn"),
    ("Mother", "indian mother porn"),
    ("Young", "young porn"),
    ("Fuck", "fuck porn"),
    ("Wife", "indian wife porn"),
    ("Beauty", "beauty porn"),
    ("Cutie", "cute porn"),
    ("Beautiful", "beautiful porn"),
    ("College", "college porn"),
    ("Bhabhi", "bhabhi porn"),
    ("Aunty", "aunty porn"),
    ("Teen", "teen porn"),
    ("Lesbian", "lesbian porn"),
    ("Milf", "milf porn"),
    ("Anal", "anal porn"),
    ("Big Boobs", "big boobs porn"),
    ("Big Ass", "big ass porn"),
    ("HD", "hd porn"),
    ("Hindi", "hindi porn"),
    ("School", "school porn"),
    ("Group Sex", "group sex porn"),
    ("Outdoor", "outdoor porn"),
    ("Office", "office porn"),
    ("Romantic", "romantic porn"),
    ("Hardcore", "hardcore porn"),
    ("Nurse", "nurse porn"),
    ("Nude", "nude porn"),
    ("Sexy", "sexy porn"),
    ("Blowjob", "blowjob porn"),
    ("Housewife", "housewife porn"),
    ("Cousin", "cousin porn"),
    ("Teacher", "teacher porn"),
    ("Sister", "sister porn"),
    ("Stepmom", "stepmom porn"),
    ("Girlfriend", "girlfriend porn"),
    ("Mature", "mature porn"),
    ("Solo", "solo porn"),
    ("Massage", "massage porn"),
    ("Cheating", "cheating porn"),
    ("Bath", "bath porn"),
    ("Public", "public porn"),
    ("BBW", "bbw porn"),
    ("Cumshot", "cumshot porn"),
    ("POV", "pov porn"),
    ("Gangbang", "gangbang porn"),
    ("Creampie", "creampie porn"),
    ("Double Penetration", "double penetration porn"),
    ("Interracial", "interracial porn"),
    ("Japanese", "japanese porn"),
    ("Korean", "korean porn"),
    ("Chinese", "chinese porn"),
    ("Russian", "russian porn"),
    ("Pakistani", "pakistani porn"),
    ("Bangladeshi", "bangladeshi porn"),
    ("Nepali", "nepali porn"),
    ("Sri Lankan", "sri lankan porn"),
    ("Punjabi", "punjabi porn"),
    ("Tamil", "tamil porn"),
    ("Telugu", "telugu porn"),
    ("Bengali", "bengali porn"),
    ("Marathi", "marathi porn"),
    ("Kannada", "kannada porn"),
    ("Gujarati", "gujarati porn"),
]

def scrape_video(title):
    for url_template in SEARCH_SITES:
        url = url_template.format(title)
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            thumbs = soup.find_all("div", class_="thumb-block")
            if not thumbs:
                thumbs = soup.find_all("div", class_="video")
            if not thumbs:
                thumbs = soup.find_all("div", class_="video-thumb")
            if thumbs:
                selected = random.choice(thumbs)
                a_tag = selected.find("a", href=True)
                video_url = a_tag["href"] if a_tag else None
                if video_url and not video_url.startswith("http"):
                    if "xnxx.com" in url:
                        video_url = "https://www.xnxx.com" + video_url
                    elif "xvideos.com" in url:
                        video_url = "https://www.xvideos.com" + video_url
                    elif "xhamster.com" in url:
                        video_url = "https://xhamster.com" + video_url
                    elif "pornhub.com" in url:
                        video_url = "https://www.pornhub.com" + video_url
                    elif "porn.com" in url:
                        video_url = "https://www.porn.com" + video_url
                    elif "fuq.com" in url:
                        video_url = "https://www.fuq.com" + video_url
                    elif "tube8.com" in url:
                        video_url = "https://www.tube8.com" + video_url
                    elif "youporn.com" in url:
                        video_url = "https://www.youporn.com" + video_url
                    elif "spankbang.com" in url:
                        video_url = "https://spankbang.com" + video_url
                    elif "redtube.com" in url:
                        video_url = "https://www.redtube.com" + video_url
                return video_url
        except Exception as e:
            print(f"Scraping error: {e}")
    return None

app = Client("pornbot_categories", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("pornstart"))
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

for idx, (display, search_term) in enumerate(PORN_CATEGORIES):
    async def handler(client, query, search_term=search_term, display=display):
        video = scrape_video(search_term)
        if video:
            await query.message.reply(f"{display}: [Watch here]({video})", disable_web_page_preview=False)
        else:
            await query.message.reply(f"No video found for {display}.")
        await query.answer()
    app.on_callback_query(filters.regex(f"^porn_{idx}$"))(handler)

if __name__ == "__main__":
    app.run()
