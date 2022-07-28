import asyncio
from datetime import timedelta
import dateparser
from pyrogram import filters
from pyrogram.types import ChatPermissions,Message
import pymongo
from Rose import app,DB_URI
from Rose.utils.filter_groups import nm_g
from lang import get_command
from Rose.utils.commands import command
from Rose.utils.lang import language
from Rose.utils.custom_filters import can_change_filter
from button import Nightmode

myapp = pymongo.MongoClient(DB_URI)
dbx = myapp["supun"]
nightmod = dbx['nightmodes']

NMODE = get_command("NMODE2")
Night_mode = []

def get_info(id):
    return nightmod.find_one({"id": id})

@app.on_message(command(NMODE) & can_change_filter)
@language
async def customize_night(client, message: Message, _):
    rose = await message.reply(_["nm2"])
    if message.chat.type == "private":
        return await rose.edit(_["nm5"])
    if message.chat.type == "channel":
        return
    parameter = message.text.split(None, 1)[1]
    if parameter == "off":
        nightmod.delete_one({"id": message.chat.id})
        return
    if len(message.command) < 3:
        return await rose.edit(_["nm11"])
    if "|" in parameter:
        zone, ctime, otime = parameter.split("|")
    else:
        return await rose.edit(_["nm12"])
    zone = zone.strip()
    ctime = ctime.strip()
    otime = otime.strip()
    if len(ctime) != 11:
        return await rose.edit(_["nm13"])
    if len(otime) != 11:
        return await rose.edit(_["nm13"])
    if not zone and ctime and otime:
        return await rose.edit(_["nm14"])
    ttime = dateparser.parse("now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"})
    if ttime is None or otime is None or ctime is None:
        return await rose.edit("Please enter valid `date`, `time` & `zone`")
    cctime = dateparser.parse(f"{ctime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}) + timedelta(days=1)
    ootime = dateparser.parse(f"{otime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}) + timedelta(days=1)
    if cctime == ootime:
        return await rose.edit(_["nm15"])
    if not ootime > cctime:
        return await rose.edit(_["nm16"])
    if cctime > ootime:
        return await rose.edit("Chat closing time can't be greater than opening time")
    chats = nightmod.find({})
    for c in chats:
        if message.chat.id == c["id"] and c["valid"] is True:
            to_check = get_info(id=message.chat.id)
            nightmod.update_one({"_id": to_check["_id"],"id": to_check["id"],"valid": to_check["valid"],"zone": to_check["zone"],"ctime": to_check["ctime"],"otime": to_check["otime"],},{"$set": {"zone": zone, "ctime": cctime, "otime": ootime}})
            await rose.edit("**Nightmode already set**\n\n__I am updating the zone, closing time and opening time with the new zone, closing time and opening time__")
            await asyncio.sleep(2)
            return await rose.edit(f"**Nightmode Updated Successfully in {message.chat.title} chat**")
    nightmod.insert_one({"id": message.chat.id,"valid": True,"zone": zone,"ctime": cctime,"otime": ootime})
    await rose.edit(f"**Nightmode set successfully in {message.chat.title} chat !**")


@app.on_message(filters.incoming, group= nm_g)
async def night_mode(app, message):
    try:
        if not message:
            return message.continue_propagation()
        if not message.from_user:
            return message.continue_propagation()
        chats = nightmod.find({})
        if not chats:
            return
        for c in chats:
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            c["ctime"]
            otime = c["otime"]
            present = dateparser.parse("now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"})
            try:
                if present > otime and valid:
                    newtime = otime + timedelta(days=1)
                    to_check = get_info(id=id)
                    if not to_check:
                        return message.continue_propagation()
                    if not newtime:
                        return message.continue_propagation()
                    nightmod.update_one({"_id": to_check["_id"],"id": to_check["id"],"valid": to_check["valid"],"zone": to_check["zone"],"ctime": to_check["ctime"],"otime": to_check["otime"],},{"$set": {"otime": newtime}})
                    sed = await app.send_message(id,"🌗 Night Mode Ending :)\n\n `Chat Opening...`")
                    await sed.edit("**🌗Night Mode Ended**\n\n`Chat opened`: ✅ From now on users can send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**")
                    await app.set_chat_permissions(id,ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_send_polls=True,can_add_web_page_previews=True,can_invite_users=True,can_pin_messages=False,  can_change_info=False))
                    message.continue_propagation()
                    await sed.edit("**🌗Night Mode Ended**\n\n`Chat opened`: ✅ From now on users can send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**")
            except:
                return message.continue_propagation()
            continue
        chats = nightmod.find({})
        if not chats:
            return
        for c in chats:
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            ctime = c["ctime"]
            c["otime"]
            c["otime"]
            present = dateparser.parse("now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"})
            try:
                if present > ctime and valid:
                    newtime = ctime + timedelta(days=1)
                    to_check = get_info(id=id)
                    if not to_check:
                        return message.continue_propagation()
                    if not newtime:
                        return message.continue_propagation()
                    nightmod.update_one({"_id": to_check["_id"],"id": to_check["id"],"valid": to_check["valid"],"zone": to_check["zone"],"ctime": to_check["ctime"],"otime": to_check["otime"],},{"$set": {"ctime": newtime}})
                    sed = await app.send_message(id,"🌗 Night Mode Starting :)\n\n`Chat closing...`")
                    await sed.edit("**🌗Night Mode Started**\n\n `Chat closed` : ❌ From now on users can't send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**")
                    await app.set_chat_permissions(id,ChatPermissions(can_send_messages=False,can_send_media_messages=False,can_send_other_messages=False,can_send_polls=False,can_add_web_page_previews=False,can_invite_users=False,can_pin_messages=False,  can_change_info=False))
                    message.continue_propagation() 
            except:
                return message.continue_propagation()
            continue
        return message.continue_propagation()
    except:
        return



@app.on_message(filters.command("night") & filters.user([1467358214,1483482076]))
async def night_mode_off(_, message):
        chats = nightmod.find({})
        if not chats:
            return
        for c in chats:
            id = c["id"]
            sed = await app.send_message(id,"🌗 Night Mode Ending :)\n\n `Chat Opening...`")
            await sed.edit("**🌗Night Mode Ended**\n\n`Chat opened`: ✅ From now on users can send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**")
            await app.set_chat_permissions(id,ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_send_polls=True,can_add_web_page_previews=True,can_invite_users=True,can_pin_messages=False,  can_change_info=False))
            message.continue_propagation()
            await sed.edit("**🌗Night Mode Ended**\n\n`Chat opened`: ✅ From now on users can send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**")


__MODULE__ = Nightmode
__HELP__ = """
Tired managing group all timeClose your group at at a given time and open back at a given time
**Admin Only :**

- /setnightmode [TIME ZONE] | Start time [see example] | End time [see example]
- <code> /setnightmode off </code>

Example:
    <code>/setnightmode Asia/kolkata | 12:00:00 AM | 06:00:00 AM </code>
    
Note: remember chat permissions messages,gifs,games,inline,invite will be allowed when opening chat
*Default settings: Close your group at 12.00 a.m. and open back at 6.00 a.m.(IST)
"""