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
try:
    from config import (
        API_ID, API_HASH, TOKEN, BOT_LOGGING, DATABASE_ID, FORCE_JOIN,
        MONGO_URL, BACKUP_MONGO_URL, DB_NAME, SUPPORT_CHAT, UPDATE_CHAT, OWNER_ID,
        MUST_JOIN, IMGBB_API_KEY, START_MEDIA, PHOTO_URL, STATS_IMG, CHARA_CHANNEL_ID
    )
except ImportError:
    # Fallback to lowercase variable names if legacy config is used
    from config import (
        api_id as API_ID, api_hash as API_HASH, TOKEN, BOT_LOGGING, DATABASE_ID, FORCE_JOIN,
        mongo_url as MONGO_URL, backup_mongo_url as BACKUP_MONGO_URL, DB_NAME, 
        SUPPORT_CHAT, UPDATE_CHAT, OWNER_ID, MUSJ_JOIN as MUST_JOIN, 
        IMGBB_API_KEY, START_MEDIA, PHOTO_URL, STATS_IMG, CHARA_CHANNEL_ID
    )

# 🧪 CRITICAL TOKEN VALIDATION CHECK
if not TOKEN or TOKEN.strip() == "" or "Botfather" in TOKEN:
    logging.error("❌ [CRITICAL] BOT_TOKEN IS EMPTY OR INVALID INSIDE CONFIG.PY / ENV!")
    print("\n🦋 Ara ara~ Host engine initialization aborted!")
    print("⚠️  The 'TOKEN' variable is missing or blank inside your configuration file.")
    print("👉 Please edit your config file or platform environment variables and insert a valid token from @BotFather.\n")
    sys.exit(1)

FORCE_JOIN_LINK = "https://t.me/+fPjchISAGnc3OGJl"  # Updated dynamically on bot startup

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
redeem_collection = db["redeem_codes"]  # Redeem codes collection

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
# Explicit module imports (Recommended over wildcard '*' imports)
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
    """Create indexes for redeem codes collection for better performance."""
    try:
        await redeem_collection.create_index("code", unique=True)
        await redeem_collection.create_index("is_active")
        await redeem_collection.create_index("creator_id")
        await redeem_collection.create_index("redeemed_count")
        await redeem_collection.create_index("reward_type")
        await redeem_collection.create_index("created_at", expireAfterSeconds=2592000)  # 30 days
        LOGGER(__name__).info("✅ Redeem collection indexes created successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Error creating redeem indexes: {e}")

async def create_user_collection_indexes():
    """Create indexes for user collection for better performance."""
    try:
        await user_collection.create_index("id", unique=True)
        await user_collection.create_index("username")
        await user_collection.create_index("characters")
        LOGGER(__name__).info("✅ User collection indexes created successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Error creating user collection indexes: {e}")

async def create_character_collection_indexes():
    """Create indexes for character collection for better performance."""
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
        
        # Create all indexes concurrently
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
    
    # Initialize database
    await initialize_database()
    
    # Timezone-aware UTC timestamp
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    
    # Log startup
    await PLOG(
        f"🦋 **Bot Started Successfully**\n"
        f"👤 **Owner:** `{OWNER_ID}`\n"
        f"📅 **Time:** {current_time} UTC"
    )
    
    LOGGER(__name__).info("✅ Bot startup complete")

# ---------------------------- END OF CODE ------------------------------
