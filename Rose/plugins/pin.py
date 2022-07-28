from html import escape as escape_html
from pyrogram.types import Message
from Rose import app,LOG_GROUP_ID
from Rose.mongo.pindb import Pins
from Rose.utils.custom_filters import admin_filter, command
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.string import build_keyboard, parse_button
from Rose.utils.lang import language
from button import Pin

@app.on_message(command("pin") & admin_filter )
@language
async def pin_message(client, message: Message, _):
    pin_args = message.text.split(None, 1)
    if message.reply_to_message:
        try:
            disable_notification = len(pin_args) < 2 or pin_args[1] not in ["alert", "notify", "loud"]
            await message.reply_to_message.pin(disable_notification=disable_notification)
            if message.chat.username:
                link_chat_id = message.chat.username
                message_link = (f"https://t.me/{link_chat_id}/{message.reply_to_message.message_id}")
            elif (str(message.chat.id)).startswith("-100"):
                link_chat_id = (str(message.chat.id)).replace("-100", "")
                message_link = (f"https://t.me/c/{link_chat_id}/{message.reply_to_message.message_id}")
            await message.reply_text(_["pin1"].format(message_link),disable_web_page_preview=True)
        except Exception as e:
            await app.send_message(LOG_GROUP_ID, text=e)
    else:
        await message.reply_text(_["pin4"])
    return


@app.on_message(command("unpin") & admin_filter)
@language
async def unpin_message(client, message: Message, _):
    try:
        if message.reply_to_message:
            await app.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
            await message.reply_text(_["pin5"])
        else:
            await app.unpin_chat_message(message.chat.id)
            await message.reply_text(_["pin6"])
    except Exception as e:
            return await app.send_message(LOG_GROUP_ID,text=e)  

@app.on_message(command("unpinall") & admin_filter)
@language
async def unpinall_message(client, message: Message, _):
    user_id = message.from_user.id
    return await message.reply_text(_["pin9"],reply_markup=ikb([[("Yes", f"unpinallcb:{user_id}"), ("No", "close_admin")]]),)
    


@app.on_message(command("antichannelpin") & admin_filter )
@language
async def anti_channel_pin(client, message: Message, _):
    pinsdb = Pins(message.chat.id)
    if len(message.text.split()) == 1:
        status = pinsdb.get_settings()["antichannelpin"]
        return await message.reply_text(_["pin15"].format(status))
    if len(message.text.split()) == 2:
        if message.command[1] in ("yes", "on", "true"):
            pinsdb.antichannelpin_on()
            msg = ("**Enabled** anti channel pins. Automatic pins from a channel will now be replaced with the previous pin.")
        elif message.command[1] in ("no", "off", "false"):
            pinsdb.antichannelpin_off()
            msg = ("**Disabled** anti channel pins. Automatic pins from a channel will not be removed.")
        else:
            return await message.reply_text(_["pin18"])
    return await message.reply_text(msg)
    


@app.on_message(command("pinned") & admin_filter )
@language
async def pinned_message(client, message: Message, _):
    chat_title = message.chat.title
    chat = await app.get_chat(chat_id=message.chat.id)
    msg_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    if chat.pinned_message:
        pinned_id = chat.pinned_message.message_id
        if message.chat.username:
            link_chat_id = message.chat.username
            message_link = f"https://t.me/{link_chat_id}/{pinned_id}"
        elif (str(message.chat.id)).startswith("-100"):
            link_chat_id = (str(message.chat.id)).replace("-100", "")
            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}"
        await message.reply_text(f"The pinned message of {escape_html(chat_title)} is [here]({message_link}).",reply_to_message_id=msg_id,disable_web_page_preview=True)
    else:
        await message.reply_text(_["pin24"])


@app.on_message(command("cleanlinked") & admin_filter )
@language
async def clean_linked(client, message: Message, _):
    pinsdb = Pins(message.chat.id)
    if len(message.text.split()) == 1:
        status = pinsdb.get_settings()["cleanlinked"]
        return await message.reply_text(_["pin19"].format(status))
    if len(message.text.split()) == 2:
        if message.command[1] in ("yes", "on", "true"):
            pinsdb.cleanlinked_on()
            msg = "Turned on CleanLinked! Now all the messages from linked channel will be deleted!"
        elif message.command[1] in ("no", "off", "false"):
            pinsdb.cleanlinked_off()
            msg = "Turned off CleanLinked! Messages from linked channel will not be deleted!"
        else:
            return await message.reply_text(_["pin18"])
    return await message.reply_text(msg)
    


@app.on_message(command("permapin") & admin_filter )
@language
async def perma_pin(client, message: Message, _):
    if message.reply_to_message or len(message.text.split()) > 1:
        if message.reply_to_message:
            text = message.reply_to_message.text
        elif len(message.text.split()) > 1:
            text = message.text.split(None, 1)[1]
        teks, button = await parse_button(text)
        button = await build_keyboard(button)
        button = ikb(button) if button else None
        z = await message.reply_text(teks, reply_markup=button)
        await z.pin()
    else:
        await message.reply_text(_["pin23"])
        await message.delete()
    return


__MODULE__ = Pin
__HELP__ = """
All the pin related commands can be found here; 
keep your chat up to date on the latest news with 
a simple pinned message!

**User commands:**
- /pinned: Get the current pinned message.

**Admin commands:**
- /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
- /permapin `<text>`: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.
- /unpinall: Unpins all pinned messages.
- /antichannelpin `<yes/no/on/off>`: Don't let telegram auto-pin linked channels. If no arguments are given, shows current setting.
- /cleanlinked `<yes/no/on/off>`: Delete messages sent by the linked channel.

**Note:** When using antichannel pins,make sure to use the /unpin command, instead of doing it manually. Otherwise, the old message will get re-pinned when the channel sends any messages.
"""
