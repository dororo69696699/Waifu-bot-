from TEAMZYRO import app, collection, rarity_map, rarity_map2
from pyrogram import filters
from TEAMZYRO.unit.zyro_rarity import get_all_rarity_limits


@app.on_message(filters.command("rarity"))
async def rarity_count(client, message):
    try:
        # 🔥 IMPORTANT: ALWAYS fetch latest rarity limits from database (NO CACHING!)
        rarity_limits = await get_all_rarity_limits()
        
        # Build the response text
        text = "❀ ᴄʜᴀʀᴀᴄᴛᴇʀ ʀᴀʀɪᴛʏ ᴄᴏᴜɴᴛ ❀\n"
        text += "─" * 24 + "\n\n"

        total = 0
        
        # Get character counts for each rarity
        rarity_counts = {}
        for rarity_no, rarity_name in rarity_map.items():
            # Get count of characters with this rarity number
            count = await collection.count_documents(
                {"rarity_number": rarity_no}
            )
            rarity_counts[rarity_name] = count
            total += count

        # Display each rarity with its count and limit
        for rarity_name in rarity_map.values():
            count = rarity_counts.get(rarity_name, 0)
            # Get limit from database (fresh data)
            limit = rarity_limits.get(rarity_name, "∞")
            
            # Get emoji from rarity_map2
            emoji = rarity_map2.get(rarity_name, "❀")
            
            text += (
                f"{emoji} {rarity_name}\n"
                f"   ⤷ {count} ᴄʜᴀʀᴀᴄᴛᴇʀꜱ (Limit: {limit})\n\n"
            )

        text += "─" * 24 + "\n"
        text += f"❀ ᴛᴏᴛᴀʟ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ : {total}\n"
        text += "❀ ꜱʜɪɴᴏʙᴜ ᴋᴏᴄʜᴏᴜ ɪꜱ ᴡᴀᴛᴄʜɪɴɢ ʏᴏᴜ 🌸"

        await message.reply_text(text)

    except Exception as e:
        await message.reply_text(
            f"❀ ᴇʀʀᴏʀ : `{e}`"
        )
