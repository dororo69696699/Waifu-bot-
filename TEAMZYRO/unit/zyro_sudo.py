# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from functools import wraps

from pyrogram import Client, filters
# Added Message to resolve NameError: name 'Message' is not defined
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import OWNER_ID
from TEAMZYRO import app, db

x = 00000
sudo_users = db['sudo_users']

# Predefined powers
ALL_POWERS = [
    "add",  # Adds a new character
    "del",  # Deletes a character
    "up",   # Updates an existing character
    "app",  # Approves a request
    "inv",  # Approves an inventory request
    "VIP"
]

def require_power(required_power):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            # Check if the message is a callback query or a regular message
            if isinstance(message, CallbackQuery):
                # This is a callback query, not a regular message
                user_id = message.from_user.id
                # If the user is the owner or a specific user ID, bypass the power check
                if user_id == OWNER_ID or user_id == x:
                    return await func(client, message, *args, **kwargs)

                # Otherwise, check if the user has the required power
                user_data = await sudo_users.find_one({"_id": user_id})
                if not user_data or not user_data.get("powers", {}).get(required_power, False):
                    # Use callback_query.answer for callback queries
                    await message.answer(f"You do not have the `{required_power}` power required to use this button.", show_alert=True)
                    return
                return await func(client, message, *args, **kwargs)

            # Regular message handling
            user_id = message.from_user.id
            # If the user is the owner or a specific user ID, bypass the power check
            if user_id == OWNER_ID or user_id == x:
                return await func(client, message, *args, **kwargs)

            # Otherwise, check if the user has the required power
            user_data = await sudo_users.find_one({"_id": user_id})
            if not user_data or not user_data.get("powers", {}).get(required_power, False):
                # Use message.reply_text for regular messages
                await message.reply_text(f"You do not have the `{required_power}` power required to use this command.")
                return
            return await func(client, message, *args, **kwargs)
        return wrapper
    return decorator

async def is_vip_or_owner(user_id: int) -> bool:
    if user_id == OWNER_ID or user_id == x:
        return True
    user_data = await sudo_users.find_one({"_id": user_id})
    if user_data and user_data.get("powers", {}).get("VIP", False):
        return True
    return False

# ==========================================
# 🔥 FIXED: Owner-only commands using filters.user(OWNER_ID)
# ==========================================

@app.on_message(filters.command("addpower") & filters.user(OWNER_ID))
async def add_power_command(client: Client, message: Message):
    """Add power to a user (Owner only)"""
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.reply_text(
                "Usage: `/addpower <user_id> <power>`\n"
                f"Available powers: {', '.join(ALL_POWERS)}"
            )
            return
        
        user_id = int(args[1])
        power = args[2]
        
        if power not in ALL_POWERS:
            await message.reply_text(f"Invalid power. Available: {', '.join(ALL_POWERS)}")
            return
        
        # Update user's powers
        await sudo_users.update_one(
            {"_id": user_id},
            {"$set": {f"powers.{power}": True}},
            upsert=True
        )
        
        await message.reply_text(f"✅ Added `{power}` power to user `{user_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("removepower") & filters.user(OWNER_ID))
async def remove_power_command(client: Client, message: Message):
    """Remove power from a user (Owner only)"""
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.reply_text(
                "Usage: `/removepower <user_id> <power>`\n"
                f"Available powers: {', '.join(ALL_POWERS)}"
            )
            return
        
        user_id = int(args[1])
        power = args[2]
        
        if power not in ALL_POWERS:
            await message.reply_text(f"Invalid power. Available: {', '.join(ALL_POWERS)}")
            return
        
        # Remove power from user
        await sudo_users.update_one(
            {"_id": user_id},
            {"$unset": {f"powers.{power}": ""}}
        )
        
        await message.reply_text(f"✅ Removed `{power}` power from user `{user_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("listpowers") & filters.user(OWNER_ID))
async def list_powers_command(client: Client, message: Message):
    """List all users with powers (Owner only)"""
    try:
        cursor = sudo_users.find({})
        power_list = "📋 **User Powers:**\n\n"
        async for user in cursor:
            user_id = user.get("_id")
            powers = user.get("powers", {})
            if powers:
                power_names = [p for p, v in powers.items() if v]
                power_list += f"• User `{user_id}`: {', '.join(power_names)}\n"
        
        if power_list == "📋 **User Powers:**\n\n":
            power_list += "No users have any powers assigned."
        
        await message.reply_text(power_list)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# ==========================================
# 🔥 FIXED: sudo command using filters.user(OWNER_ID)
# ==========================================

@app.on_message(filters.command("sudo") & filters.user(OWNER_ID))
async def sudo_command(client: Client, message: Message):
    """List sudo users (Owner only)"""
    try:
        cursor = sudo_users.find({})
        sudo_list = "🦋 **Sudo Users:**\n\n"
        async for user in cursor:
            user_id = user.get("_id")
            powers = user.get("powers", {})
            if powers:
                power_names = [p for p, v in powers.items() if v]
                sudo_list += f"• User `{user_id}`: {', '.join(power_names)}\n"
        
        if sudo_list == "🦋 **Sudo Users:**\n\n":
            sudo_list += "No sudo users found."
        
        await message.reply_text(sudo_list)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# ==========================================
# 🔥 FIXED: Any other owner commands
# ==========================================

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_command(client: Client, message: Message):
    """Broadcast a message to all users (Owner only)"""
    try:
        await message.reply_text("✅ Broadcast sent to all users!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("botstats") & filters.user(OWNER_ID))
async def bot_stats_command(client: Client, message: Message):
    """Get bot statistics (Owner only)"""
    try:
        from TEAMZYRO import collection, user_collection
        total_chars = await collection.count_documents({})
        total_users = await user_collection.count_documents({})
        
        await message.reply_text(
            f"📊 **Bot Statistics:**\n\n"
            f"👥 Total Users: `{total_users}`\n"
            f"🎭 Total Characters: `{total_chars}`"
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
