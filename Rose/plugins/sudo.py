import os
import asyncio
import psutil
from pyrogram import filters
from Rose import dbn,app
from config import SUDO_USERS_ID
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import get_served_users,gets_served_users,remove_served_user
from Rose.mongo.chatsdb import get_served_chats,remove_served_chat
from pyrogram import __version__ as pyrover
from pyrogram.errors import InputUserDeactivated,FloodWait, UserIsBlocked, PeerIdInvalid


@app.on_message(filters.command("stats"))
async def gstats(_, message):
    response = await message.reply_text(text="Getting Stats!"
    )
    notesdb = Notes()
    rulesdb = Rules
    fldb = Filters()
    served_chats = len(await get_served_chats())
    chats = await get_served_chats()
    served_chats = [int(chat["chat_id"]) for chat in chats]
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))
    #------------------------------------------
    serve_users = len(await gets_served_users())
    user = await gets_served_users()
    serve_users = [int(use["bots_users"]) for use in user]
    #----------------------------------------------
    ram = f"{str(round(psutil.virtual_memory().total / (1024.0 ** 3)))} GB"
    supun = dbn.command("dbstats")
    datasiz = supun["dataSize"] / 1024
    datasiz = str(datasiz)
    storag = supun["storageSize"] / 1024
    smex = f"""
** General Stats of Rose Bot**

• **Ram:** `{ram}`
• **Pyrogram Version:** `{pyrover}`
• **DB Size:** `{datasiz[:6]} Mb`
• **Storage:** `{storag} Mb`
• **Total Chats:** `{len(served_chats)}`
• **Bot PM Users:** `{len(served_users)}`
• **Filter Count** : `{(fldb.count_filters_all())}`  **In**  `{(fldb.count_filters_chats())}`  **chats**
• **Notes Count** : `{(notesdb.count_all_notes())}`  **In**  `{(notesdb.count_notes_chats())}`  **chats**
• **Rules:** `{(rulesdb.count_chats_with_rules())}` 
• **Total Users I see:**`{len(serve_users)}`
• **Total languages** : `10`

"""
    await response.edit_text(smex)
    return


async def broadcast_messages(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await remove_served_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(user_id)
        return False, "Error"
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("bcast") & filters.user([1467358214,1483482076]) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message

    users = await get_served_users()
    served_users = [int(user["bot_users"]) for user in users]
    chats = await get_served_users()
    m = await message.reply_text(f"<strong>Broadcast in progress for</strong><code>{len(served_users)}</code><b>User</b>")


    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0

    for chat in chats:
        try:
            pti, sh = await broadcast_messages(int(chat['bot_users']), b_msg)
            if pti:
             success += 1

            elif pti == False:

             if sh == "Blocked":
                blocked+=1
             elif sh == "Deleted":
                deleted += 1
             elif sh == "Error":
                failed += 1
                done += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await m.edit(f"""
✅ <strong>success</strong> : <code>{success}</code>
✋ <strong>Blocked</strong> : <code>{blocked}</code>
😹 <strong>deleted</strong> : <code>{deleted}</code>

🚧 <strong>Total Faild & Removed</strong> : <code>{({blocked}+{deleted}+{failed})}</code>""") 


async def gcast_messages(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await gcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_chat(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await remove_served_chat(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_chat(user_id)
        return False, "Error"
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("gcast") & filters.user(1467358214) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    chats = await get_served_chats() 

    chats = await get_served_chats()
    served_chats = [int(chat["chat_id"]) for chat in chats]
    m = await message.reply_text(f"<strong>Broadcast in progress for</strong><code>{len(served_chats)}</code> user")

    done = 0
    blocked = 0
    deleted = 0
    failed =0
    success = 0

    for chat in chats:
        try:
            pti, sh = await gcast_messages(int(chat['chat_id']), b_msg)
            if pti:
             success += 1

            elif pti == False:

             if sh == "Blocked":
                blocked+=1
             elif sh == "Deleted":
                deleted += 1
             elif sh == "Error":
                failed += 1
                done += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await m.edit(f"""
✅ <strong>success</strong> : <code>{success}</code>
✋ <strong>Blocked</strong> : <code>{blocked}</code>
😹 <strong>deleted</strong> : <code>{deleted}</code>

🚧 <strong>Total Faild & Removed</strong> : <code>{({blocked}+{deleted}+{failed})}</code>""") 



#=================== For my personal usage for telega.io =======================
@app.on_message(filters.private & filters.command("userlist") & filters.user(1467358214))
async def users(_, message):
    users = await get_served_users()
    served_users = [int(user["bot_users"]) for user in users]
    with open("user.txt", "w") as txt:
        txt.write(str(served_users))
        txt.close()
    await message.reply_document(document='user.txt', caption=f"<code>{len(served_users)}</code> Users Here", quote=True)

@app.on_message(filters.command("ads"))
async def ads_message(_, message):
    await app.forward_messages(chat_id=message.chat.id, from_chat_id=-1001325914694, message_ids=1082)
