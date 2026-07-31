# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message
import html
from TEAMZYRO import *
import asyncio
from pyrogram import enums
from TEAMZYRO.unit.zyro_rarity import rarity_map, rarity_map2

async def get_user_stats(user_id):
    # Fetch user data
    user_data = await user_collection.find_one({'id': user_id}, {'balance': 1, 'first_name': 1, 'characters': 1})
    if not user_data:
        return None, "User data not found."
    
    balance = user_data.get('balance', 0)
    first_name = html.escape(user_data.get('first_name', 'Unknown'))
    characters = user_data.get('characters', [])
    
    # Calculate total characters in collection
    total_characters = await collection.count_documents({})
    
    # Calculate character count and collection progress
    character_count = len(characters)
    progress_percentage = (character_count / total_characters * 100) if total_characters > 0 else 0
    
    # Create progress bar
    progress_bar_length = 10
    filled_slots = int(progress_percentage / 100 * progress_bar_length)
    progress_bar = '█' * filled_slots + '□' * (progress_bar_length - filled_slots)
    
    # Fetch global rank
    cursor = user_collection.find({}, {"_id": 0, "id": 1, "characters": 1})
    all_users = await cursor.to_list(length=None)
    all_users.sort(key=lambda x: len(x.get('characters', [])), reverse=True)
    total_users = len(all_users)
    rank = next((i + 1 for i, user in enumerate(all_users) if user['id'] == user_id), total_users)
    
    # 🔥 FIX: Count characters by rarity dynamically using rarity_map
    # Initialize all rarities with 0
    rarity_counts = {rarity: 0 for rarity in rarity_map.values()}
    
    # Count characters
    for char in characters:
        # Get the rarity from the character data
        char_rarity = char.get('rarity')
        if char_rarity and char_rarity in rarity_counts:
            rarity_counts[char_rarity] += 1
    
    return {
        'user_id': user_id,
        'first_name': first_name,
        'balance': balance,
        'character_count': character_count,
        'total_characters': total_characters,
        'progress_percentage': progress_percentage,
        'progress_bar': progress_bar,
        'rank': rank,
        'total_users': total_users,
        'rarity_counts': rarity_counts
    }, None

@app.on_message(filters.command("stats"))
async def stats_handler(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Send initial "Processing..." message with the image
    processing_message = await message.reply_photo(
        photo=STATS_IMG[0],
        caption="Processing...",
        parse_mode=enums.ParseMode.HTML
    )
    
    # Small delay to simulate processing
    await asyncio.sleep(1)
    
    stats, error = await get_user_stats(user_id)
    
    if error:
        await processing_message.edit_caption(caption=error, parse_mode=enums.ParseMode.HTML)
        return
    
    # Get rarity counts
    rarity_counts = stats['rarity_counts']
    
    # 🔥 FIX: Build the stats dynamically with ALL rarities from rarity_map
    # Get the emoji for each rarity
    rarity_display = []
    for rarity_name in rarity_map.values():
        emoji = rarity_map2.get(rarity_name, '')
        count = rarity_counts.get(rarity_name, 0)
        # Format the display name without emoji for cleanliness
        display_name = rarity_name.replace('⚪️ ', '').replace('🟣 ', '').replace('🟢 ', '').replace('🟡 ', '')
        display_name = display_name.replace('💮 ', '').replace('🔮 ', '').replace('💸 ', '').replace('🌤 ', '')
        display_name = display_name.replace('🎐 ', '').replace('❄️ ', '').replace('💝 ', '').replace('🎃 ', '')
        display_name = display_name.replace('🎄 ', '').replace('🧧 ', '').replace('🍑 ', '').replace('🎗️ ', '')
        display_name = display_name.replace('🌧 ', '').replace('🦠 ', '')
        rarity_display.append(f"{emoji} <b>{display_name}</b>{' ' * (20 - len(display_name))}↬ {count}")
    
    # Join all rarity lines
    rarity_lines = "\n".join(rarity_display)
    
    # Build the stats caption with Shinobu theme
    stats_message = (
        f"🦋 <b>𝐒꯭𝒉꯭𝛊꯭𝒏꯭𝒐꯭𝒃꯭𝒖 𝐆𝐚𝐫𝐝𝐞𝐧</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>𝐍𝐚𝐦𝐞</b>        ↬ {stats['first_name']}\n"
        f"🆔 <b>𝐔𝐬𝐞𝐫 𝐈𝐃</b>     ↬ {stats['user_id']}\n\n"
        f"🌸 <b>𝐖𝐢𝐬𝐭𝐞𝐫𝐢𝐚 𝐏𝐞𝐭𝐚𝐥𝐬</b> ↬ {stats['balance']}\n"
        f"🦋 <b>𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧</b>      ↬ {stats['character_count']}/{stats['total_characters']}\n"
        f"🏆 <b>𝐆𝐥𝐨𝐛𝐚𝐥 𝐑𝐚𝐧𝐤</b>     ↬ #{stats['rank']}\n\n"
        f"📈 <b>𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐢𝐨𝐧</b> ↬ {stats['progress_bar']} {stats['progress_percentage']:.1f}%\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{rarity_lines}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🌸\n"
        f"<i>\"Every butterfly eventually finds\n"
        f"its place beneath the wisteria.\"</i>\n\n"
        f"💜 <b>Shinobu Kocho</b>"
    )
    
    # Edit the processing message with the final stats
    await processing_message.edit_caption(
        caption=stats_message,
        parse_mode=enums.ParseMode.HTML
    )
