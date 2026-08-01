# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import asyncio
import importlib
import logging
import sys

from TEAMZYRO import *
from TEAMZYRO.modules import ALL_MODULES

# Safe fallback imports in case MUST_JOIN/FORCE_JOIN are named differently in config
try:
    from config import MUST_JOIN
except ImportError:
    MUST_JOIN = getattr(sys.modules[__name__], "FORCE_JOIN", None)


async def initialize_bot():
    """Initialize bot and database asynchronously."""
    LOGGER("TEAMZYRO").info("🦋 Initializing WaifuBot...")
    
    # Load all modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚 𝐛𝐲🥳...")
    
    # Initialize database
    LOGGER("TEAMZYRO").info("🔄 Initializing database connections and indexes...")
    try:
        if "initialize_database" in globals():
            await initialize_database()
            LOGGER("TEAMZYRO").info("✅ Database initialization complete")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"❌ Database initialization failed: {e}")
        LOGGER("TEAMZYRO").warning("⚠️ Continuing with potentially slower queries...")
    
    return True


def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize bot asynchronously
    try:
        loop.run_until_complete(initialize_bot())
    except Exception as e:
        LOGGER("TEAMZYRO").critical(f"❌ Bot initialization failed: {e}")
        sys.exit(1)
    
    # Start Pyrogram Client safely
    ZYRO.start()

    # Verify FORCE_JOIN / MUST_JOIN target safely
    target_join = getattr(sys.modules[__name__], "FORCE_JOIN", MUST_JOIN)
    
    if target_join:
        try:
            try:
                chat_target = int(target_join)
            except ValueError:
                chat_target = target_join
                
            chat_obj = ZYRO.get_chat(chat_target)
            invite_link = chat_obj.invite_link
            if not invite_link:
                invite = ZYRO.create_chat_invite_link(chat_target)
                invite_link = invite.invite_link
                
            LOGGER("TEAMZYRO").info(f"Successfully verified FORCE_JOIN admin rights. Link: {invite_link}")
        except Exception as e:
            LOGGER("TEAMZYRO").error(
                "\n"
                "=======================================================================\n"
                "❌ CRITICAL STARTUP ERROR:\n"
                f"Bot is NOT an admin in the FORCE_JOIN channel/chat ({target_join})!\n"
                "Please ensure the bot is added to the channel as an Admin.\n"
                f"Details: {e}\n"
                "======================================================================="
            )
            try:
                ZYRO.stop()
            except Exception:
                pass
            sys.exit(1)

    # Verify BOT_LOGGING permissions
    bot_logging_id = globals().get("BOT_LOGGING", None)
    if bot_logging_id:
        try:
            try:
                log_target = int(bot_logging_id)
            except ValueError:
                log_target = bot_logging_id
                
            test_msg = ZYRO.send_message(
                chat_id=log_target,
                text="⚙️ **WaifuBot Startup Notification**:\n"
                     "✅ Successfully connected & verified write permissions in the logs channel!\n"
                     "✅ Database indexes initialized successfully!\n"
                     "🦋 Bot is ready to serve!"
            )
            LOGGER("TEAMZYRO").info(f"Successfully verified BOT_LOGGING permissions. Test message sent (ID: {test_msg.id}).")
        except Exception as e:
            LOGGER("TEAMZYRO").error(
                "\n"
                "=======================================================================\n"
                "❌ CRITICAL STARTUP ERROR:\n"
                f"Bot cannot post/send messages to BOT_LOGGING chat ({bot_logging_id})!\n"
                "Details: {e}\n"
                "======================================================================="
            )
            try:
                ZYRO.stop()
            except Exception:
                pass
            sys.exit(1)

    # Send optional start notification function if declared
    if "send_start_message" in globals():
        try:
            send_start_message()
        except Exception as e:
            LOGGER("TEAMZYRO").warning(f"Could not send startup message: {e}")
    
    # Idle loop
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY TEAMEGOIST☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    
    from pyrogram import idle
    idle()
    ZYRO.stop()


if __name__ == "__main__":
    main()
