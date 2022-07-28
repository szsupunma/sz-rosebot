import asyncio
from  Rose import app
from Rose.mongo.captcha import captchas
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions,Message
from pyrogram import filters
from . antlangs import get_arg
from lang import get_command
from Rose.utils.commands import command
from Rose.utils.lang import language
from Rose.utils.custom_filters import restrict_filter
from button import Extra

CAPTCH = get_command("CAPTCH")
REMOVEC = get_command("REMOVEC")
db = {}

@app.on_message(command(CAPTCH) & ~filters.private & restrict_filter)
@language
async def add_chat(client, message: Message, _):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = await app.get_chat_member(chat_id, user_id)
    if user.status in ["administrator", "creator"]:
      chat = captchas().chat_in_db(chat_id)
      if chat:
            await message.reply_text(_["capt1"])
      else:
           await message.reply_text(text=_["capt2"],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Captcha On ✅", callback_data=f"new_{chat_id}_{user_id}_E"),InlineKeyboardButton(text="Captcha Off ❌", callback_data=f"off_{chat_id}_{user_id}")],[InlineKeyboardButton(text="Close Menu ✖️", callback_data=f"close_data")]]))
      args = get_arg(message)
      lower_args = args.lower()
      if lower_args == "on":     
        await message.reply_text(text=_["capt2"],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Captcha On ✅", callback_data=f"new_{chat_id}_{user_id}_E"),InlineKeyboardButton(text="Captcha Off ❌", callback_data=f"off_{chat_id}_{user_id}")],[InlineKeyboardButton(text="Close Menu ✖️", callback_data=f"close_data")]]))  
      if lower_args == "off":     
           await message.reply_text(text=_["capt2"],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Captcha On ✅", callback_data=f"new_{chat_id}_{user_id}_E"),InlineKeyboardButton(text="Captcha Off ❌", callback_data=f"off_{chat_id}_{user_id}")],[InlineKeyboardButton(text="Close Menu ✖️", callback_data=f"close_data")]]))                                                      
      
async def send_captcha(app,message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat = captchas().chat_in_db(chat_id)
    if not chat:
        return
    try:
        user_s = await app.get_chat_member(chat_id, user_id)
        if (user_s.is_member is False) and (db.get(user_id, None) is not None):
            try:
                await app.delete_messages(chat_id=chat_id,message_ids=db[user_id]["msg_id"])
            except:
                pass
            return
        elif (user_s.is_member is False):
            return
    except UserNotParticipant:
        return
    chat_member = await app.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
        if chat_member.restricted_by.id == (await app.get_me()).id:
            pass
        else:
            return
    try:
        if db.get(user_id, None) is not None:
            try:
                await app.send_message(chat_id=chat_id,text=f"❗️ {message.from_user.mention} again joined group without verifying!\n\n""He can try again after 5 minutes.",disable_web_page_preview=True)
                await app.delete_messages(chat_id=chat_id,message_ids=db[user_id]["msg_id"])
            except:
                pass
            await asyncio.sleep(300)
            del db[user_id]
    except:
        pass
    try:
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except:
        return
    await app.send_message(chat_id,text=f"🙋‍♀️ Hi {message.from_user.mention}, welcome to {message.chat.title} group chat!\n\n To continue, first verify that you're not a robot. ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🤖 Verify Now ", callback_data=f"verify_{chat_id}_{user_id}"),InlineKeyboardButton(text="Pass ❗️", callback_data=f"_unmute_{user_id}")]]))
    return 400

@app.on_message(command(REMOVEC) & ~filters.private)
@language
async def del_chat(client, message: Message, _):
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ["administrator", "creator"]:
        j = captchas().delete_chat(chat_id)
        if j:
            await message.reply_text(_["capt3"])

__MODULE__ = Extra
__HELP__ = """
**Commands:**
 - /id: Get the id of user or chat.
 - /info: Get basic information of a user.
 - /paste: Paste given text on a website.
 - /tr [lang code]: Translate text messages.
 - /q : To quote a message.
 - /q [INTEGER] : To quote more than 1 messages.
 - /q r : to quote a message with it's reply
 - /telegraph <reply to jpg, jpeg, png, gif or mp4>: upload to telegraph.
 - /tm <reply to jpg, jpeg, png, gif or mp4>: upload to telegraph.
 - /tgm <reply to jpg, jpeg, png, gif or mp4>: upload to telegraph.
 - /invitelink: Get invitelink for your group.
 
**Example:*
 - Translate text message to English:
> `/tr en` [Reply some text message]
"""