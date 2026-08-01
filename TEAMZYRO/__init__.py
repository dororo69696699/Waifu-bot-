# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

# ------------------------------ IMPORTS ---------------------------------
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone

from aiogram import Bot, Dispatcher, types
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, enums
from pyrogram import filters as f
from telegram.ext import Application

# --------------------------- LOGGING SETUP ------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telegram").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# ---------------------------- CONFIGURATION -----------------------------
import config

# Helper function to safely fetch attributes regardless of typo/case variations
def get_config_var(*names, default=None):
    for name in names:
        if hasattr(config, name):
            return getattr(config, name)
    return default

API_ID = get_config_var("API_ID", "api_id")
API_HASH = get_config_var("API_HASH", "api_hash")
TOKEN = get_config_var("TOKEN", "token", "BOT_TOKEN")
BOT_LOGGING = get_config_var("BOT_LOGGING", "bot_logging")
DATABASE_ID = get_config_var("DATABASE_ID", "database_id")
FORCE_JOIN = get_config_var("FORCE_JOIN", "force_join")
MONGO_URL = get_config_var("MONGO_URL", "mongo_url")
BACKUP_MONGO_URL = get_config_var("BACKUP_MONGO_URL", "backup_mongo_url")
DB_NAME = get_config_var("DB_NAME", "db_name")
SUPPORT_CHAT = get_config_var("SUPPORT_CHAT", "support_chat")
UPDATE_CHAT = get_config_var("UPDATE_CHAT", "update_chat")
OWNER_ID = get_config_var("OWNER_ID", "owner_id")

# Handled your 'musj' typo here safely:
MUST_JOIN = get_config_var("MUSJ_JOIN", "musj_join", "MUST_JOIN", "must_join")

IMGBB_API_KEY = get_config_var("IMGBB_API_KEY", "imgbb_api_key")
START_MEDIA = get_config_var("START_MEDIA", "start_media")
PHOTO_URL = get_config_var("PHOTO_URL", "photo_url")
STATS_IMG = get_config_var("STATS_IMG", "stats_img")
CHARA_CHANNEL_ID = get_config_var("CHARA_CHANNEL_ID", "chara_channel_id")

# 🧪 CRITICAL TOKEN VALIDATION CHECK
if not TOKEN or str(TOKEN).strip() == "" or "Botfather" in str(TOKEN):
    logging.error("❌ [CRITICAL] BOT_TOKEN IS EMPTY OR INVALID INSIDE CONFIG.PY / ENV!")
    print("\n🦋 Ara ara~ Host engine initialization aborted!")
    print("⚠️  The 'TOKEN' variable is missing or blank inside your configuration file.")
    print("👉 Please edit your config file or platform environment variables and insert a valid token from @BotFather.\n")
    sys.exit(1)

FORCE_JOIN_LINK = "https://t.me/+fPjchISAGnc3OGJl"

# --------------------- TELEGRAM BOT CONFIGURATION -----------------------
command_filter = f.create(lambda _, __, message: bool(message.text and message.text.startswith("/")))

application = Application.builder().token(TOKEN).build()
ZYRO = Client("Shivu", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------------- DATABASE SETUP ------------------------------
ddw = AsyncIOMotorClient(MONGO_URL)
db = ddw[DB_NAME]

collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
discounts_collection = db['discounts']
redeem_collection = db["redeem_codes"]

backup_ddw = AsyncIOMotorClient(BACKUP_MONGO_URL) if BACKUP_MONGO_URL else None

# -------------------------- GLOBAL VARIABLES ----------------------------
app = ZYRO
x = 0000000

# --------------------------- STORAGE DICTS ------------------------------
locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
user_cooldowns = {}
user_nguess_progress = {}
user_guess_progress = {}
normal_message_counts = {}  

# -------------------------- POWER SETUP --------------------------------
try:
    from TEAMZYRO.unit import (
        zyro_ban,
        zyro_sudo,
        zyro_react,
        zyro_log,
        zyro_send_img,
        zyro_rarity,
    )
except ImportError as err:
    LOGGER(__name__).warning(f"⚠️ Non-critical module import warning: {err}")

# ------------------------------------------------------------------------

async def PLOG(text: str):
    """Send log messages to the logging channel."""
    try:
        await app.send_message(
            chat_id=BOT_LOGGING,
            text=f"🦋 <b>[LAB LOG]:</b>\n{text}",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        LOGGER(__name__).error(f"Failed to send log message: {e}")

# ==========================================
# DATABASE INITIALIZATION & INDEXES
# ==========================================

async def create_redeem_indexes():
    """Create indexes for redeem codes collection."""
    try:
        await redeem_collection.create_index("code", unique=True)
        await redeem_collection.create_index("is_active")
        await redeem_collection.create_index("creator_id")
        await redeem_collection.create_index("redeemed_count")
        await redeem_collection.create_index("reward_type")
        await redeem_collection.create_index("created_at", expireAfterSeconds=2592000)
        LOGGER(__name__).info("✅ Redeem collection indexes created successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Error creating redeem indexes: {e}")

async def create_user_collection_indexes():
    """Create indexes for user collection."""
    try:
        await user_collection.create_index("id", unique=True)
        await user_collection.create_index("username")
        await user_collection.create_index("characters")
        LOGGER(__name__).info("✅ User collection indexes created successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Error creating user collection indexes: {e}")

async def create_character_collection_indexes():
    """Create indexes for character collection."""
    try:
        await collection.create_index("id", unique=True)
        await collection.create_index("anime")
        await collection.create_index("rarity")
        await collection.create_index([("anime", 1), ("rarity", 1)])
        LOGGER(__name__).info("✅ Character collection indexes created successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Error creating character collection indexes: {e}")

async def initialize_database():
    """Initialize all database collections and indexes."""
    try:
        LOGGER(__name__).info("🔄 Initializing database collections...")
        
        await asyncio.gather(
            create_redeem_indexes(),
            create_user_collection_indexes(),
            create_character_collection_indexes()
        )
        
        LOGGER(__name__).info("✅ Database initialization complete")
        await PLOG("✅ **Database Initialization Complete**\nAll collections and indexes have been set up successfully.")
        
    except Exception as e:
        LOGGER(__name__).error(f"❌ Database initialization error: {e}")
        await PLOG(f"❌ **Database Initialization Failed**\nError: `{str(e)}`")

# ==========================================
# BOT STARTUP HANDLER
# ==========================================

async def on_startup():
    """Function to run when bot starts."""
    LOGGER(__name__).info("🦋 Bot is starting up...")
    
    await initialize_database()
    
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    
    await PLOG(
        f"🦋 **Bot Started Successfully**\n"
        f"👤 **Owner:** `{OWNER_ID}`\n"
        f"📅 **Time:** {current_time} UTC"
    )
    
    LOGGER(__name__).info("✅ Bot startup complete")

# ---------------------------- END OF CODE ------------------------------
