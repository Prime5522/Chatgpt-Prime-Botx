from typing import List
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.client import Client
from info import *


async def get_fsub(bot: Client, message: Message) -> bool:
    """
    Checks if the user is a subscriber of the channel and if not asks him to join the channel.

    Parameters:
    bot (Client): The client instance.
    message (Message): The message that triggered the function.

    Returns:
    bool: True if the user is a subscriber, False otherwise.
    """
    target_channel_id = AUTH_CHANNEL  # Your channel ID
    user_id = message.from_user.id

    try:
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        channel_link: str = (await bot.get_chat(target_channel_id)).invite_link  # type: ignore
        join_button = InlineKeyboardButton("✇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇", url=channel_link)  # type: ignore
        try_again_button = InlineKeyboardButton(
            "🔄 Tʀʏ Aɢᴀɪɴ ♻️", 
            url="https://t.me/Prime_ChatGPT_ProBot?start=start"
        )
        
        keyboard: List[List[InlineKeyboardButton]] = [[join_button], [try_again_button]]

        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://envs.sh/KgA.jpg",  # Replace with your image link
            caption=(
                "Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ ғɪʀꜱᴛ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n\n"
                "ғɪʀꜱᴛ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '✇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇' ʙᴜᴛᴛᴏɴ, ᴛʜᴇɴ, "
                "ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ 'ʀᴇǫᴜᴇꜱᴛ ᴛᴏ Jᴏɪɴ' ʙᴜᴛᴛᴏɴ.\n\n"
                "ᴀғᴛᴇʀ ᴛʜᴀᴛ ᴄᴏᴍᴇ ʜᴇʀᴇ ᴀɢᴀɪɴ ᴀɴᴅ 🔄 ᴄʟɪᴄᴋ ᴛᴏ Tʀʏ Aɢᴀɪɴ ♻️."
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    return True
