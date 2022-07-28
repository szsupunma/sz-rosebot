import asyncio
import pymongo
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions
from Rose.mongo.locksdb import (
    b_on,
    b_off,
    is_b_on,
    remove_chat,
)
from Rose import app, app as pbot, MONGO_URL as  MONGO_DB_URI,LOG_GROUP_ID
from Rose.utils.custom_filters import admin_filter
from button import Locks
from Rose.core.decorators.permissions import current_chat_permissions,member_permissions


#====== Mongo database =========
client = pymongo.MongoClient(MONGO_DB_URI)
dbd = client["szrosebot"]
db = dbd
lockdb = db.lockdb1
#================================

data = {
    "video": "vid",
    "audio": "aud",
    "document": "doc",
    "forward": "fwd",
    "photo": "pic",
    "sticker": "stc",
    "gif": "gif",
    "games": "game",
    "album": "albm",
    "voice": "voice",
    "video_note": "vnote",
    "contact": "contact",
    "location": "gps",
    "address": "address",
    "reply": "reply",
    "message": "message",
    "comment": "cmt",
    "edit": "edit",
    "mention": "mention",
    "inline": "inline",
    "polls": "poll",
    "dice": "dice",    
    "buttons": "button",
    "media": "media",
    "email": "emal", 
    "url":"url",
    "spoiler":"spoiler",
    "anonchannel":"anonchannel",
    "channel":"channel",
    "porn":"porn",
    "spam":"spam",
}

incorrect_parameters = "<b>Incorrect lock types send </b><code>/locktypes</code><b> to see all.</b>"

permdata = {
    "send_messages": "can_send_messages",
    "send_stickers": "can_send_stickers",
    "send_gifs": "can_send_animations",
    "send_media": "can_send_media_messages",
    "send_games": "can_send_games",
    "send_inline": "can_use_inline_bots",
    "url_prev": "can_add_web_page_previews",
    "send_polls": "can_send_polls",
    "change_info": "can_change_info",
    "invite_user": "can_invite_users",
    "pin_messages": "can_pin_messages",
}

array1= ["channel","spam","porn","anonchannel","spoiler","url","vid", "aud","doc", "fwd","pic", "stc", "gif", "game","albm", "voice", "vnote","contact","gps", "address", "reply","message","cmt","edit","mention","inline", "poll", "dice", "button", "media", "emal",]
array2= ["channel","spam","porn","anonchannel","spoiler","url","video", "audio","document", "forward","photo", "sticker", "gif", "games","album", "voice", "video_note","contact","location", "address", "reply","message","comment","edit","mention","inline", "polls", "dice", "buttons", "media", "email",]

array3 =["send_messages","send_stickers","send_gifs","send_media","send_games","send_inline","url_prev","send_polls","change_info","invite_user", "pin_messages","all_permissions"]
array4=["can_send_messages","can_send_stickers","can_send_animations","can_send_media_messages","can_send_games","can_use_inline_bots","can_add_web_page_previews","can_send_polls","can_invite_users","can_change_info","can_pin_messages"]
array5=["send_messages","send_stickers","send_gifs","send_media","send_games","send_inline","url_prev","send_polls","invite_user","change_info","pin_messages"]


async def tg_lock(message, permissions: list, perm: str, lock: bool):
    if lock:
        if perm not in permissions:
            return await message.reply_text("Already locked.")
    elif perm in permissions:
        return await message.reply_text("Already Unlocked.")
    (permissions.remove(perm) if lock else permissions.append(perm))
    permissions = {perm: True for perm in list(set(permissions))}
    try:
        await pbot.set_chat_permissions(message.chat.id, ChatPermissions(**permissions))
    except ChatNotModified:
        return await message.reply_text("<b>To unlock this, you have to unlock</b><code>messages</code><b>first.</b>")


@pbot.on_message(filters.command("lock") & ~filters.private & ~filters.via_bot & admin_filter)
async def lock(_, message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        if len(message.command) != 2:
            return await message.reply("<b>Send something.. ): what do you want to lock in this chat ?</b>")
        parameter = message.text.strip().split(None, 1)[1].lower()
        state = message.command[0].lower()
        permissions = await member_permissions(chat_id, user_id)
        if "can_restrict_members" not in permissions:
            return await message.reply_text(f"{message.from_user.mention},You need to be an admin with <b>restrict members<b> permission.")
        permissions = await current_chat_permissions(chat_id)
        if parameter in permdata:
            await tg_lock(message, permissions, permdata[parameter], state == "lock")
            return await message.reply_text((f"<b>Locked</b> {parameter}." if state == "lock" else f"<b>Unlocked</b> {parameter}."))
        elif parameter == "all_permissions" and state == "lock":
            await _.set_chat_permissions(chat_id, ChatPermissions())
            await message.reply_text("Locked All Permissions.")
        elif parameter == "all_permissions" and state == "unlock":   
            for i in range((len(array4))-2):
                await tg_lock(message, permissions, array4[i], state == "lock")
            return await message.reply("All permissions unlocked")
        elif parameter in data and state == "lock":
            if okletsgo := lockdb.find_one({f"{data[parameter]}": message.chat.id}):
                await message.reply(f"{parameter} already locked")
            else:
                lockdb.insert_one({f"{data[parameter]}": message.chat.id})
                await message.reply(f"Locked {parameter}")
            return
        elif parameter in data and state == "unlock":
            if okletsgo := lockdb.find_one({f"{data[parameter]}": message.chat.id}):
                lockdb.delete_one({f"{data[parameter]}": message.chat.id})
                await message.reply(f"Unocked {parameter}")
            else:
                await message.reply(f"{parameter} already unlocked")
            return
        elif parameter == "all" and state == "lock":
            for i in range(len(array1)):
                isittrue = lockdb.find_one({f"{array1[i]}": message.chat.id})
                if not isittrue:
                    lockdb.insert_one({f"{array1[i]}": message.chat.id})
            return await message.reply_text("Locked Everything.")
        elif parameter == "bots" and state == "lock":

            if await is_b_on(chat_id):
                return await message.reply_text("Bots already locked.")
            await b_on(chat_id)
            await message.reply_text("Locked bots.")
        elif parameter == "bots" and state == "unlock":
            if await is_b_on(chat_id):
                await b_off(chat_id) 
                await message.reply_text("Unlocked bots.")  
            else:
                await message.reply_text("Bots not locked.")
        elif parameter == "all" and state == "unlock":
            for i in range(len(array1)):
                if isittrue := lockdb.find_one({f"{array1[i]}": message.chat.id}):
                    lockdb.delete_one({f"{array1[i]}": message.chat.id})
            if await is_b_on(chat_id):
                await b_off(chat_id)
            Escobar = remove_chat(int(message.chat.id))
            return await message.reply_text("unLocked all.")
        else:
            return await message.reply(incorrect_parameters)

    except Exception as e:
        await app.send_message(chat_id=LOG_GROUP_ID, text=e)
        print(e)


@pbot.on_message(filters.command("locks") & ~filters.private)
async def list_locks_dfunc(_, message):
    user_id = message.from_user.id
    text = f"**These are the locks in this chat:**\n"
    for i in range(len(array1)):
        isittrue = lockdb.find_one({f"{array1[i]}": message.chat.id})
        if isittrue:
            text += f" • {array2[i]} = `Locked `\n" 
        else:
            text += f" • {array2[i]} = `None`\n"
    await message.reply_text(text)
    try:
        await app.send_message(chat_id = user_id,text = text)
    except Exception as e:
        supun = await app.send_message( chat_id = message.chat.id,text = f"Hey {message.from_user.mention} please start me pm now.")
        await asyncio.sleep(5)
        await supun.delete()
        await app.send_message(chat_id = LOG_GROUP_ID,text=e)
        print(e)    


@pbot.on_message(filters.command("locktypes") & ~filters.private)
async def wew(_, message):
    lol = "**Locktypes available for this chat:  ** \n"
    for i in range(len(array2)):
        lol += f" • {array2[i]}\n"
    lol += "\n • all"
    await message.reply(lol)





__MODULE__ = Locks
__HELP__ = """
**Locks**
Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!
The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

**Admin commands:**
- /lock <item(s)>: Lock one or more items. Now, only admins can use this type!
- /unlock <item(s)>: Unlock one or more items. Everyone can use this type again!
- /locks: List currently locked items.
- /locktypes: Show the list of all lockable items.

**Examples:**
- Lock stickers with:
• `/lock sticker`
- You can lock/unlock multiple items by chaining them:
• `/lock sticker photo gif video`
"""
__helpbtns__ = (
        [[InlineKeyboardButton("Lock Types", callback_data="_ucd"),            
          InlineKeyboardButton("Permissions Locks", callback_data="_kcd")],
        [InlineKeyboardButton("Examples", callback_data="_lcd")]])
