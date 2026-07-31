# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import ReturnDocument
from TEAMZYRO import collection, app, user_collection, require_power, db
from TEAMZYRO.unit.zyro_rarity import rarity_map, update_rarity_limit, get_rarity_limit, get_all_rarity_limits
from config import OWNER_ID  # 🔥 ADD THIS IMPORT

@app.on_message(filters.command("gdelete"))
@require_power("del")
async def delete_handler(client, message):
    try:
        # Extract arguments from the command
        args = message.text.split()
        if len(args) != 2:
            await message.reply_text("Incorrect format... Please use: /gdelete ID")
            return

        character_id = args[1]

        # Find and delete the character from the main collection
        character = await collection.find_one_and_delete({'id': character_id})
        if character:
            # Remove the character from all users' collections
            update_result = await user_collection.update_many(
                {'characters.id': character_id},
                {'$pull': {'characters': {'id': character_id}}}
            )

            await message.reply_text(
                f"Character with ID {character_id} deleted successfully from the database.\n"
                f"Removed from {update_result.modified_count} user collections."
            )
        else:
            await message.reply_text(f"Character with ID {character_id} not found in the database.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

import time

@app.on_message(filters.command("gupdate"))
@require_power("up")
async def update(client: Client, message: Message):
    try:
        args = message.text.split()
        if len(args) != 4:
            await message.reply_text('Incorrect format. Please use: /gupdate id field new_value')
            return

        character_id = args[1]
        field_to_update = args[2]
        new_value = args[3]

        # Validate field
        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if field_to_update not in valid_fields:
            await message.reply_text(f'Invalid field. Please use one of the following: {", ".join(valid_fields)}')
            return

        # Process the new value
        if field_to_update in ['name', 'anime']:
            new_value = new_value.replace('-', ' ').title()
        elif field_to_update == 'rarity':
            try:
                new_value = rarity_map[int(new_value)]  # Use rarity_map
            except (KeyError, ValueError):
                await message.reply_text('Invalid rarity. Please use a valid number between 1-12 for rarity.')
                return

        # Update the character in the main collection
        result = await collection.update_one({'id': character_id}, {'$set': {field_to_update: new_value}})
        if result.modified_count == 0:
            await message.reply_text('Character not found or no changes made.')
            return

        # Fetch users who have the character
        users_cursor = user_collection.find({'characters.id': character_id})
        total_users = await user_collection.count_documents({'characters.id': character_id})

        if total_users == 0:
            await message.reply_text('sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇ ✅')
            return

        # Send initial message for progress
        progress_message = await message.reply_text('Updating: 0% completed...')
        updated_count = 0
        progress_threshold = 10  # Show progress every 10%
        next_progress_update = progress_threshold

        async for user in users_cursor:
            await user_collection.update_one(
                {'_id': user['_id'], 'characters.id': character_id},
                {'$set': {f'characters.$.{field_to_update}': new_value}}
            )
            updated_count += 1

            # Show progress at every 10% interval
            progress = (updated_count / total_users) * 100
            if progress >= next_progress_update:
                await progress_message.edit_text(f'Updating: {int(progress)}% completed...')
                next_progress_update += progress_threshold
                time.sleep(1)  # Add a 1-second delay

        # Final message with the total count
        await progress_message.edit_text('Updating: 100% completed.')
        await message.reply_text(f'sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇ ✅ \nTotal users updated: {updated_count}/{total_users}')

    except Exception as e:
        await message.reply_text(f'Error: {str(e)}')

import time

@app.on_message(filters.command("maxupdate"))
@require_power("up")
async def update_rarity_limit_command(client: Client, message: Message):
    """
    UPDATE RARITY MAXIMUM LIMITS
    Usage: /maxupdate <rarity_name> <new_limit>
    Example: /maxupdate "💸 Premium Edition" 10
    """
    try:
        args = message.text.split(maxsplit=2)  # Split into 3 parts max
        if len(args) != 3:
            # Show available rarities
            rarity_list = "\n".join([f"• {name}" for name in rarity_map.values()])
            await message.reply_text(
                f"❌ **Incorrect format.**\n\n"
                f"Usage: `/maxupdate <rarity_name> <new_limit>`\n"
                f"Example: `/maxupdate \"💸 Premium Edition\" 10`\n\n"
                f"**Available Rarities:**\n{rarity_list}"
            )
            return

        rarity_name = args[1].strip()
        try:
            new_limit = int(args[2].strip())
        except ValueError:
            await message.reply_text("❌ New limit must be a valid number")
            return

        if new_limit < 0:
            await message.reply_text("❌ Limit cannot be negative")
            return

        # Verify the rarity exists
        if rarity_name not in rarity_map.values():
            # Try to find matching rarity (case-insensitive, partial match)
            found_rarity = None
            for name in rarity_map.values():
                if rarity_name.lower() in name.lower():
                    found_rarity = name
                    break
            
            if found_rarity:
                rarity_name = found_rarity
            else:
                await message.reply_text(
                    f"❌ Rarity '{rarity_name}' not found.\n\n"
                    f"**Available Rarities:**\n" + "\n".join([f"• {name}" for name in rarity_map.values()])
                )
                return

        # Update in database
        success = await update_rarity_limit(rarity_name, new_limit)
        
        if success:
            # Verify the update by fetching fresh data
            updated_limit = await get_rarity_limit(rarity_name)
            await message.reply_text(
                f"✅ **Successfully updated rarity limit**\n\n"
                f"📊 **Rarity:** `{rarity_name}`\n"
                f"📈 **New Limit:** `{updated_limit}`\n\n"
                f"Run `/rarity` to see all current limits."
            )
        else:
            await message.reply_text(f"❌ Failed to update limit for '{rarity_name}'. Please try again.")
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# ==========================================
# 🔥 FIXED: /resetrarities now uses filters.user(OWNER_ID)
# ==========================================

@app.on_message(filters.command("resetrarities") & filters.user(OWNER_ID))
async def reset_rarities_command(client: Client, message: Message):
    """Reset all rarity limits to default values (Owner only)"""
    try:
        collection = db['rarity_limits']
        # Delete all existing limits
        await collection.delete_many({})
        # Initialize with defaults
        from TEAMZYRO.unit.zyro_rarity import initialize_rarity_limits
        await initialize_rarity_limits()
        
        await message.reply_text(
            "✅ **All rarity limits have been reset to defaults**\n"
            "Run `/rarity` to see the default limits."
        )
    except Exception as e:
        await message.reply_text(f"❌ Error resetting limits: {str(e)}")
