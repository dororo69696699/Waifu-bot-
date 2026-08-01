import os
import random
import time
from pyrogram import Client, enums, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from TEAMZYRO import *
from TEAMZYRO.unit.zyro_help import HELP_DATA

START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# Private Start Message Generator
async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name
    
    msg_date = getattr(message, "date", None)
    ping = round(time.time() - msg_date.timestamp(), 2) if msg_date else 0.0
    uptime = get_uptime()

    caption = (
        f"🌸 <b>ᴀʀᴀ ᴀʀᴀ~ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ!</b> 🌸\n\n"
        f"<i>ɪ ᴀᴍ {bot_name}. ɪᴛ sᴇᴇᴍs ʏᴏᴜ'ᴠᴇ ᴡᴀɴᴅᴇʀᴇᴅ sᴛʀᴀɪɢʜᴛ ɪɴᴛᴏ ᴍʏ ʟᴀʙᴏʀᴀᴛᴏʀʏ. ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ, ᴛʜᴇ ғʀᴇsʜ ᴡɪsᴛᴇʀɪᴀ ғʀᴀɢʀᴀɴᴄᴇ ᴡɪʟʟ ᴋᴇᴇᴘ ʏᴏᴜ sᴀғᴇ ғʀᴏᴍ ᴀɴʏ ɴᴀsᴛʏ ᴅᴇᴍᴏɴs ʜᴇʀᴇ.</i>\n\n"
        f"<blockquote>━━━━━━━▧▣▧━━━━━━━\n"
        f"⦾ <b>ᴍɪssɪᴏɴ:</b> ɪ ᴛʀᴀᴄᴋ ᴅᴏᴡɴ ʀᴏᴀᴍɪɴɢ sʟᴀʏᴇʀs ᴀɴᴅ ᴛʀᴀᴘ ᴡᴀɴᴅᴇʀɪɴɢ ᴅᴇᴍᴏɴs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛs.\n"
        f"⦾ <b>ᴛʀᴀɪɴɪɴɢ:</b> ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴜsᴇ /help ᴛᴏ ʀᴇᴀᴅ ᴍʏ ᴄᴜsᴛᴏᴍ ᴛʀᴀɪɴɪɴɢ ᴍᴀɴᴜᴀʟs.\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"⚡ <b>ᴘᴜʟsᴇ:</b> <code>{ping}</code> ᴍs\n"
        f"⏳ <b>ʀᴇsᴛ ᴢᴏɴᴇ:</b> <code>{uptime}</code></blockquote>"
    )

    buttons = [
        [InlineKeyboardButton("🦋 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [
            InlineKeyboardButton("💜 sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ],
        [
            InlineKeyboardButton("🧪 ʜᴇʟᴘ", callback_data="open_help"),
            InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/EGOIST_6969")
        ]
    ]

    return caption, buttons

# Group Start Message Generator
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = (
        f"🦋 <i>ғʟᴀᴘ, ғʟᴀᴘ... ɪ ᴀᴍ</i> <b>{bot_user.first_name}</b> 🌸\n\n"
        f"<blockquote>ɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴍᴏɴɪᴛᴏʀɪɴɢ ᴛʜɪs ᴄʜᴀᴛ ᴀʀᴇᴀ ᴛᴏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ᴇxᴘᴏsᴇ ʜɪᴅᴅᴇɴ ᴅᴇᴍᴏɴs ᴛʜʀᴏᴜɢʜ ᴍᴇssᴀɢᴇ ғʟᴏᴡs.\n\n"
        f"ᴜsᴇ /help ᴛᴏ ᴀᴄᴄᴇss ᴍʏ sᴘᴇᴄɪᴀʟɪᴢᴇᴅ ᴍᴇᴅɪᴄᴀʟ ᴀɴᴅ ᴄᴏᴍʙᴀᴛ ᴍᴀɴᴜᴀʟs!</blockquote>"
    )
    buttons = [
        [
            InlineKeyboardButton("💜 sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ]
    ]
    return caption, buttons

# Send Media Helper
async def send_media_message(message, media, caption, buttons):
    if media.lower().endswith(('.png', '.jpg', '.jpeg')):
        await message.reply_photo(photo=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)
    elif media.lower().endswith('.gif'):
        await message.reply_animation(animation=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_video(video=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)

# Private Start Command Handler
@app.on_message(filters.command("start") & filters.private)
async def start_private_command(client, message):
    existing_user = await user_collection.find_one({"id": message.from_user.id})

    if not existing_user:
        user_data = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "start_time": time.time()
        }
        await user_collection.insert_one(user_data)

    caption, buttons = await generate_start_message(client, message)
    
    start_media_list = globals().get("START_MEDIA", [])
    media = random.choice(start_media_list) if start_media_list else "https://telegra.ph/file/default.jpg"

    bot_logging_id = globals().get("BOT_LOGGING", None)
    if bot_logging_id:
        try:
            await app.send_message(
                chat_id=bot_logging_id,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )
        except Exception:
            pass

    await send_media_message(message, media, caption, buttons)

# Group Start Command Handler
@app.on_message(filters.command("start") & filters.group)
async def start_group_command(client, message):
    caption, buttons = await generate_group_start_message(client)
    start_media_list = globals().get("START_MEDIA", [])
    media = random.choice(start_media_list) if start_media_list else "https://telegra.ph/file/default.jpg"
    await send_media_message(message, media, caption, buttons)

def find_help_modules():
    buttons = []
    for module_name, module_data in HELP_DATA.items():
        button_name = module_data.get("HELP_NAME", "ᴜɴᴋɴᴏᴡɴ")
        buttons.append(InlineKeyboardButton(
            f"📋 {button_name}",
            callback_data=f"help_{module_name}"
        ))
    return [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

# Help Menu Callback
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton(
        "⬅️ ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɴsɪᴏɴ",
        callback_data="back_to_home"
    )])

    text = (
        "⚙️ <b>🦋 ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
        "<blockquote>sᴇʟᴇᴄᴛ ᴀ ᴛᴀʀɢᴇᴛ ᴅɪʀᴇᴄᴛᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇᴀᴅ ᴏᴜʀ ᴇxᴇᴄᴜᴛɪᴏɴ ᴍᴀɴᴜᴀʟs ᴀɴᴅ ᴛʀᴇᴀᴛᴍᴇɴᴛ ɢᴜɪᴅᴇs.\n\n"
        "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ɪɴsɪᴅᴇ ᴍᴜsᴛ ʙᴇ ᴅᴇᴘʟᴏʏᴇᴅ ᴜsɪɴɢ ᴛʜᴇ ᴘʀᴇғɪx sʏᴍʙᴏʟ: <code>/</code></blockquote>"
    )

    try:
        await query.message.edit_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

# Module Help Callback
@app.on_callback_query(filters.regex(r"^help_(.+)"))
async def show_help(client, query: CallbackQuery):
    module_name = query.data.split("_", 1)[1]
    try:
        module_data = HELP_DATA.get(module_name, {})
        help_text = module_data.get("HELP", "ɪs ᴍᴏᴅᴜʟᴇ ᴋᴀ ᴋᴏɪ ʜᴇʟᴘ ɴᴀʜɪ ʜᴀɪ.")
        buttons = [[InlineKeyboardButton(
            "⬅️ ʙᴀᴄᴋ ᴛᴏ ʟᴀʙᴏʀᴀᴛᴏʀʏ",
            callback_data="open_help"
        )]]

        full_text = (
            f"🧪 <b>{module_name.upper()} ᴄʟɪɴɪᴄᴀʟ ʀᴇᴄᴏʀᴅs:</b>\n\n"
            f"<blockquote>{help_text}</blockquote>"
        )

        try:
            await query.message.edit_caption(
                caption=full_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await query.message.edit_text(
                text=full_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
    except Exception:
        await query.answer("ᴀɴᴛɪᴅᴏᴛᴇ ʟᴏɢs ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ʟᴏᴀᴅᴇᴅ ᴘʀᴏᴘᴇʀʟʏ!", show_alert=True)

# Return to Home Callback
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query: CallbackQuery):
    caption, buttons = await generate_start_message(client, query.message)
    try:
        await query.message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await query.message.edit_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
