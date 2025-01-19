import asyncio
import random
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import FloodWait
from info import *
from plugins.utils import create_image, get_ai_response 
from .db import *
from .fsub import get_fsub

@Client.on_message(filters.command("start") & filters.incoming) # type:ignore
async def startcmd(client: Client, message: Message):
    userMention = message.from_user.mention()
    if await users.get_user(message.from_user.id) is None:
        await users.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if FSUB and not await get_fsub(client, message): return
    
    # React with emoji
    await message.react(emoji="🔥", big=True)

    # Send sticker and delete after 3 seconds
    m = await message.reply_sticker("CAACAgUAAxkBAAJ_9GcBHjuwkFd321YlOG4WOtdDCLv7AAIhFAACTiwJVPNa_9D21RH6NgQ")
    await asyncio.sleep(3)
    await m.delete()

    # Inline keyboard with buttons
    keyboard = [
        [InlineKeyboardButton("✨ ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ ⚡", url="https://t.me/Prime_Movies4U"), InlineKeyboardButton("💬 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 💬", url="https://t.me/Prime_botz_Support")],
        [InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ 📢", url="https://t.me/Prime_botz")],
        [InlineKeyboardButton("☆ 💫 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 💫 ☆", url="https://t.me/Prime_Nayem")]
    ]

    # Send photo with caption and inline keyboard
    await message.reply_photo(
        photo="https://envs.sh/HGx.jpg",
        caption=f"<b>Hello Dear 👋 {userMention},\n\nIᴍ Hᴇʀᴇ Tᴏ Rᴇᴅᴜᴄᴇ Yᴏᴜʀ Pʀᴏʙʟᴇᴍs..\nYᴏᴜ Cᴀɴ Usᴇ Mᴇ As ʏᴏᴜʀ Pʀɪᴠᴀᴛᴇ Assɪsᴛᴀɴᴛ..\nAsᴋ Mᴇ Aɴʏᴛʜɪɴɢ...Dɪʀᴇᴄᴛʟʏ..\n\n<blockquote> 🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ  <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛz 🔥</a></blockquote></b>",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return


@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN)) # type:ignore
async def broadcasting_func(client : Client, message: Message):
    msg = await message.reply_text("Wait a second!") # type:ignore
    if not message.reply_to_message:
        return await msg.edit("<b>Please reply to a message to broadcast.</b>")
    await msg.edit("Processing ...")
    completed = 0
    failed = 0
    to_copy_msg = message.reply_to_message
    users_list = await users.get_all_users()
    for i , userDoc in enumerate(users_list):
        if i % 20 == 0:
            await msg.edit(f"Total : {i} \nCompleted : {completed} \nFailed : {failed}")
        user_id = userDoc.get("user_id")
        if not user_id:
            continue
        try:
            await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/Prime_botz_Support')]]))
            completed += 1
        except FloodWait as e:
            if isinstance(e.value , int | float):
                await asyncio.sleep(e.value)
                await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/Prime_botz_Support')]]))
                completed += 1
        except Exception as e:
            print("Error in broadcasting:", e) 
            failed += 1
            pass
    await msg.edit(f"Successfully Broadcasted\nTotal : {len(users_list)} \nCompleted : {completed} \nFailed : {failed}")
    

@Client.on_message(filters.command("ai"))  # Remove the filters.chat(CHAT_GROUP)
async def grp_ai(client: Client, message: Message):
    query: str | None = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not query:
        return await message.reply_text(  # type:ignore
            "<b>Hey Buddy, use /ai followed by a question or statement!\n\nExample:\n<code>/ai Who is Allah?</code>\n\nTry it now!</b>"
        )
    if FSUB and not await get_fsub(client, message): 
        return
    message.text = query  # type:ignore
    return await ai_res(client, message)



@Client.on_message(filters.command("reset") &  filters.private) # type:ignore
async def reset(client: Client, message: Message):
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        is_reset = await chat_history.reset_history(message.from_user.id)
        if not is_reset:
            return await message.reply_text("Unable to reset chat history.") # type:ignore
        await message.reply_text("<b>Chat history has been reset.</b>") # type:ignore
    except Exception as e:
        print("Error in reset: ", e)
        return await message.reply_text("Sorry, Failed to reset chat history.If you will face any problem❔\n you contact our support group <a href='https://t.me/Prime_Botz_Support'>ᴘʀɪᴍᴇ ʙᴏᴛz suᴘᴘoʀᴛ</a>") # type:ignore


@Client.on_message(filters.command("gen") & filters.private)  # type:ignore
async def gen_image(client: Client, message: Message):
    """
    Handles private messages with the /gen command and generates an image based on the provided prompt.
    
    Args:
        client (Client): The Client object.
        message (Message): The Message object.

    Returns:
        None
    """
    sticker = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        prompt = message.text.replace("/gen", "").strip()
        encoded_prompt = prompt.replace("\n", " ")
        if not prompt:
            return await message.reply_text("Please provide a prompt.\n Example Use:\n<code>/gen Create a Beautiful Bird image</code>....\n\nHope you got it.Try it now..") # type:ignore
        image_file = await create_image(encoded_prompt)
        if not image_file:
            return await message.reply_text("Failed to generate image.") # type:ignore
        await message.reply_photo(photo=image_file , caption=f"Generated Image for prompt: {prompt[:150]}... \n Generated By @Prime_Botz") # type:ignore
        image_file.close()
    except Exception as e:
        print("Error in gen_image: ", e)
        return await message.reply_text("Sorry, I am not Available right now. If you will face any problem❔\n you contact our support group <a href='https://t.me/Prime_Botz_Support'>ᴘʀɪᴍᴇ ʙᴏᴛz suᴘᴘoʀᴛ</a>") # type:ignore
    finally:
        if sticker:await sticker.delete()

@Client.on_message(filters.text & filters.incoming & filters.private) # type:ignore
async def ai_res(client: Client, message: Message ):
    """
    Handles private text messages and sends AI responses back.
    """
    sticker = None
    reply = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        text = message.text
        if text.startswith('/'):
            return
        user_id = message.from_user.id
        history = await chat_history.get_history(user_id)
        history.append({"role": "user", "content": text})
        reply = await get_ai_response(history)
        history.append({"role": "assistant", "content": reply})
        await message.reply_text(reply) # type:ignore
        await chat_history.add_history(user_id, history)
    except Exception as e:
        print("Error in ai_res: ", e)
        reply = "Sorry, I am not available right now.If you will face any problem❔\n you contact our support group <a href='https://t.me/Prime_Botz_Support'>ᴘʀɪᴍᴇ ʙᴏᴛz suᴘᴘoʀᴛ</a>"
        await message.reply_text(reply) # type:ignore
    finally:
        if sticker:
            await sticker.delete()
