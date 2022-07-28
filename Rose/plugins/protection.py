
import requests
from Rose import app
from os import remove         
from Rose.utils.commands import command
from pyrogram.types import Message

@app.on_message(command("nsfwscan"))
async def nsfw_scan_command(_, message: Message):
    err = "Reply to an image/document/sticker/animation to scan it."
    if not message.reply_to_message:
        await message.reply_text(err)
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(err)
        return
    m = await message.reply_text("Scanning")
    file_id = get_file_id(reply)
    if not file_id:
        return await m.edit("Something went wrong.")
    file = await app.download_media(file_id)
    try:
        data = requests.post("https://api.safone.tech/nsfw", files={'image': open(file, 'rb')}).json()
        is_nsfw = data['data']['is_nsfw']
        hentai = data['data']['hentai']
        drawings = data['data']['drawings']
        porn = data['data']['porn']
        sexy = data['data']['sexy']
    except Exception as e:
        return await m.edit(str(e))
    remove(file)
    await m.edit(
        f"""
**NSFW** scan Result Here ✅

==========================
• **Porn:** `{porn} %`
• **Hentai:** `{hentai} %`
• **Sexy:** `{sexy} %`
• **Drawings:** `{drawings} %`
• **NSFW:** `{is_nsfw}`
========================== """)
    

@app.on_message(command("spamscan"))
async def scanNLP(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to scan it.")
    r = message.reply_to_message
    text = r.text or r.caption
    if not text:
        return await message.reply("Can't scan that")
    data = requests.post("https://api.safone.tech/spam", json={'text': message.text}).json()
    is_spam = data['data']['is_spam']
    spam_probability = data['data']['spam_probability']
    spam = data['data']['spam']
    ham = data['data']['ham']
    msg = f"""
**SPAM** scan Result Here ✅
==========================    
• **Is Spam:** `{is_spam}`
• **Spam Probability:** `{spam_probability}` %
• **Spam:** `{spam}`
• **Ham:** `{ham}`
=========================="""
    await message.reply(msg, quote=True)

def get_file_id(message):
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ["image/png", "image/jpeg"]:
            return
        return message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            return message.sticker.thumbs[0].file_id
        return message.sticker.file_id

    if message.photo:
        return message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        return message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        return message.video.thumbs[0].file_id
  

async def admins(chat_id: int):
    return [ member.user.id
        async for member in app.iter_chat_members(chat_id, filter="administrators")]

def get_file_unique_id(message):
    m = message
    m = m.sticker or m.video or m.document or m.animation or m.photo
    if not m:
        return
    return m.file_unique_id