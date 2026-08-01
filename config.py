import os
from dotenv import load_dotenv

# Load .env file if running locally
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "31963776"))
API_HASH = os.getenv("API_HASH", "d352f599aff861566030a3cbba3a0f75")

# Bot Token (Supports both BOT_TOKEN and TOKEN variable names)
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or "8988622858:AAHamrsZ_mCiTB4L950B7k7Y8QApzcWPDRc"
BOT_TOKEN = TOKEN

# Database Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Egoist:jayesh1090@waifubot.jblumsy.mongodb.net/?appName=Waifubot")
BACKUP_MONGO_URL = os.getenv("BACKUP_MONGO_URL", MONGO_URL)
DB_NAME = os.getenv("DB_NAME", "waifucluster")

# Logging & Channels
BOT_LOGGING = os.getenv("BOT_LOGGING", "@shinobuXwaifu")
DATABASE_ID = int(os.getenv("DATABASE_ID", "-1004441358449"))
FORCE_JOIN = int(os.getenv("FORCE_JOIN", "-1004153036996"))
CHARA_CHANNEL_ID = int(os.getenv("CHARA_CHANNEL_ID", "-1004305990907"))

# Links & Community
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/shinobuXcastel")
UPDATE_CHAT = os.getenv("UPDATE_CHAT", "https://t.me/+jyTbGn6JTeQ3M2M1")
MUSJ_JOIN = os.getenv("MUSJ_JOIN", "https://t.me/DemonXwaifu")
MUST_JOIN = os.getenv("MUST_JOIN", "https://t.me/DemonXwaifu")

# Admin Users
OWNER_ID = int(os.getenv("OWNER_ID", "7974236970"))

# ImgBB Key
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "550ead1e90c77896dbc4baf9703ac3a7")

# Media Resources
START_MEDIA = [
    os.getenv("START_MEDIA_1", "https://files.catbox.moe/5zrb1a.mp4"),
    os.getenv("START_MEDIA_2", "https://files.catbox.moe/5zrb1a.mp4")
]

PHOTO_URL = [
    os.getenv("PHOTO_URL_1", "https://i.ibb.co/v6H9qNn7/file-0000000099dc71f5a902afba055b1567.png"),
    os.getenv("PHOTO_URL_2", "https://i.ibb.co/v6H9qNn7/file-0000000099dc71f5a902afba055b1567.png")
]

STATS_IMG = [
    os.getenv("STATS_IMG", "https://files.catbox.moe/gknnju.jpg")
]
