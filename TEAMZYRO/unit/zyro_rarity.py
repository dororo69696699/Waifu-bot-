# ==========================================

# ==========================================

from TEAMZYRO import db

# Original rarity mapping (unchanged)
rarity_map = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟢 Medium",
    4: "🟡 Legendary",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "💸 Premium Edition",
    8: "🌤 Summer",
    9: "🎐 Enchanted",
    10: "❄️ Frozen",
    11: "💝 Romantic",
    12: "🎃 Haunted",
    13: "🎄 Chrimsum",
    14: "🧧 Festive",
    15: "🍑 Naughty",
    16: "🎗️ AMV Edition",
    17: "🌧 Cloudy",
    18: "🦠 Mythgard",
}

# RARITY_NAMES updated according to rarity_map (unchanged)
RARITY_NAMES = [
    "⚪️ Common",
    "🟣 Rare",
    "🟢 Medium",
    "🟡 Legendary",
    "💮 Special Edition",
    "🔮 Limited Edition",
    "💸 Premium Edition",
    "🌤 Summer",
    "🎐 Enchanted",
    "❄️ Frozen",
    "💝 Romantic",
    "🎃 Haunted",
    "🎄 Chrimsum",
    "🧧 Festive",
    "🍑 Naughty",
    "🎗️ AMV Edition",
    "🌧 Cloudy",
    "🦠 Mythgard",
]

# rarity_map2 (unchanged)
rarity_map2 = {
    "⚪️ Common": "⚪️",
    "🟣 Rare": "🟣",
    "🟢 Medium": "🟢",
    "🟡 Legendary": "🟡",
    "💮 Special Edition": "💮",
    "🔮 Limited Edition": "🔮",
    "💸 Premium Edition": "💸",
    "🌤 Summer": "🌤",
    "🎐 Enchanted": "🎐",
    "❄️ Frozen": "❄️",
    "💝 Romantic": "💝",
    "🎃 Haunted": "🎃",
    "🎄 Chrimsum": "🎄",
    "🧧 Festive": "🧧",
    "🍑 Naughty": "🍑",
    "🎗️ AMV Edition": "🎗️",
    "🌧 Cloudy": "🌧",
    "🦠 Mythgard": "🦠",
}

# DEFAULT RARITY LIMITS (fallback values)
DEFAULT_RARITY_LIMITS = {
    "⚪️ Common": 100,
    "🟣 Rare": 80,
    "🟢 Medium": 60,
    "🟡 Legendary": 40,
    "💮 Special Edition": 30,
    "🔮 Limited Edition": 25,
    "💸 Premium Edition": 20,
    "🌤 Summer": 15,
    "🎐 Enchanted": 12,
    "❄️ Frozen": 10,
    "💝 Romantic": 8,
    "🎃 Haunted": 6,
    "🎄 Chrimsum": 5,
    "🧧 Festive": 4,
    "🍑 Naughty": 3,
    "🎗️ AMV Edition": 2,
    "🌧 Cloudy": 2,
    "🦠 Mythgard": 1,
}

async def get_rarity_limit(rarity_name: str) -> int:
    """Get the limit for a specific rarity from database"""
    try:
        collection = db['rarity_limits']
        doc = await collection.find_one(
            {'rarity': rarity_name}
        )
        if doc:
            return doc['limit']
        # If not found, return default
        return DEFAULT_RARITY_LIMITS.get(rarity_name, 100)
    except Exception:
        # Fallback to default if database error
        return DEFAULT_RARITY_LIMITS.get(rarity_name, 100)

async def get_all_rarity_limits():
    """Get all rarity limits from database - ALWAYS FETCH FRESH"""
    try:
        collection = db['rarity_limits']
        cursor = collection.find({})
        limits = {}
        async for doc in cursor:
            limits[doc['rarity']] = doc['limit']
        
        # If no limits in DB, initialize with defaults
        if not limits:
            await initialize_rarity_limits()
            return DEFAULT_RARITY_LIMITS.copy()
            
        return limits
    except Exception:
        return DEFAULT_RARITY_LIMITS.copy()

async def initialize_rarity_limits():
    """Initialize database with default rarity limits if empty"""
    try:
        collection = db['rarity_limits']
        count = await collection.count_documents({})
        if count == 0:
            # Insert default limits
            default_docs = [
                {'rarity': rarity, 'limit': limit}
                for rarity, limit in DEFAULT_RARITY_LIMITS.items()
            ]
            await collection.insert_many(default_docs)
            return True
        return False
    except Exception:
        return False

async def update_rarity_limit(rarity_name: str, new_limit: int) -> bool:
    """Update limit for a specific rarity in database"""
    try:
        collection = db['rarity_limits']
        result = await collection.update_one(
            {'rarity': rarity_name},
            {'$set': {'rarity': rarity_name, 'limit': new_limit}},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    except Exception:
        return False
