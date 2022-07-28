import html
import time
import uuid
import asyncio
from Rose import *
from pyrogram import filters
from Rose.mongo.feddb import (
    is_fed_exist,
    get_fed_name,
    join_fed_db,
    leave_fed_db,
    get_connected_chats,
    new_fed_db,
    get_fed_from_chat,
    is_user_fban,
    get_fed_reason,
    get_fed_owner,
    get_fed_admins,
    get_fed_from_ownerid,
    update_reason,
    user_fban,
    user_unfban,
    fed_rename_db
)
from Rose.utils.custom_filters import owner_filter
from Rose.utils.filter_groups import fban
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.functions import extract_user
from button import Federations

                                              
@app.on_message(filters.command("joinfed"))
async def JoinFeds(client, message):
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if message.chat.type != 'supergroup':
        return await message.reply("Only supergroups can join feds.")
    if len(message.command) < 2:
        return await message.reply("You need to specify which federation you're asking about by giving me a FedID!")
    st = await app.get_chat_member(group_id, userid)
    if st.status != "creator":
        return await message.reply("Only Group Creator can join new fed!")
    if not (is_fed_exist(message.command[1])):
        return await message.reply( "This FedID does not refer to an existing federation.")
    fed_id = message.command[1]
    chat_id = message.chat.id
    chat_title = html.escape(message.chat.title)
    fed_name = get_fed_name(fed_id)
    join_fed_db(chat_id, chat_title,  fed_id)
    await message.reply(f'Successfully joined the "{fed_name}" federation! ')

@app.on_message(filters.command("leavefed"))
async def leaveFeds(client, message):
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if len(message.command) < 2:
        return await message.reply("You need to specify which federation you're asking about by giving me a FedID!")
    st = await app.get_chat_member(group_id, userid)
    if st.status != "creator":
        return await message.reply("Only Group Creator can leave fed!")
    if not (is_fed_exist(message.command[1])):
        return await message.reply("This FedID does not refer to an existing federation.")
    fed_id = message.command[1]
    chat_id = message.chat.id
    chat_title = html.escape(message.chat.title)
    fed_name = get_fed_name(fed_id)
    leave_fed_db(chat_id, chat_title,  fed_id)
    await message.reply(f'Successfully left the "{fed_name}" federation! ')

@app.on_message(filters.command("fedinfo"))
async def infoFeds(client, message):
    if len(message.command) < 2:
        return await message.reply("You need to specify which federation you're asking about by giving me a FedID!")
    if not (is_fed_exist(message.command[1])):
        return await message.reply("This FedID does not refer to an existing federation.")
    fed_id = message.command[1]
    name = get_fed_name(fed_id)
    chats = get_connected_chats(fed_id)
    await message.reply(f"""
<b>Federation info</b>
<b>Name:</b> {name}
<b>ID:</b> <code>{fed_id}</code>
<b>Chats in the fed:</b> {len(chats)}""")


@app.on_message(filters.command("newfed"))
async def NewFed(client, message):
    if (message.chat.type == 'supergroup'):
        return await message.reply('Create your federation in my PM - not in a group.')
    if len(message.command) < 2:
        return await message.reply("Give your federation a name!")
    if (len(' '.join(message.command[1:])) > 60):
        return await message.reply("Your fed must be smaller than 60 words.")
    fed_name = ' '.join(message.command[1:])
    fed_id = str(uuid.uuid4())
    owner_id = message.from_user.id
    uname = message.from_user.mention
    created_time = time.ctime()
    new_fed_db(fed_name, fed_id, created_time, owner_id)
    await message.reply(f"""
<b>Congrats, you have successfully created a federation </b>

<b>Name:</b> {fed_name}
<b>ID:</><code>{fed_id}</code>
<b>Creator:</b> {uname}     
<b>Created Date</b>: {created_time}

Use this ID to join federation! eg:<code> /joinfed {fed_id}</code>""")
    await app.send_message(chat_id=LOG_GROUP_ID,text=(f"""
<b> New Federation created with FedID: </b>

<b>Name:</b> {fed_name}
<b>ID:</b> <code>{fed_id}</code>
<b>Creator:</b> {uname}     
<b>Created Date</b> {created_time}"""))


@app.on_message(filters.all & filters.group, group=fban)
async def fed_checker(client, message):
    chat_id = message.chat.id
    if not message.from_user:
        return
    user_id = message.from_user.id 
    fed_id = get_fed_from_chat(chat_id)
    if  fed_id == None:
        if is_user_fban(fed_id, user_id):
            fed_reason = get_fed_reason(fed_id, user_id)
            text = ("**This user is banned in the current federation:**\n\n"f"User: {message.from_user.mention} (`{message.from_user.id}`)\n"f"Reason: `{fed_reason}`")
            if await app.chat.ban_member(chat_id, user_id): 
                    text += '\nAction: `Banned`'
            await asyncio.sleep(1)
            await app.chat.unban_member(chat_id, user_id)
            return await message.reply(text)

@app.on_message(filters.command("fedpromote"))
async def FedPromote(client, message):
    user_id = await extract_user(message)
    owner_id = message.from_user.id
    fed_id = get_fed_from_ownerid(owner_id)
    fed_name = get_fed_name(owner_id=owner_id)
    user = await app.get_users(user_ids=user_id)
    if (message.chat.type == 'private'):
        return await message.reply("This command is made to be run in a group where the person you would like to promote is present.")
    if fed_id is None:
        return await message.reply("Only federation creators can promote people, and you don't even seem to have a federation to promote to!")
    if (is_user_fban(fed_id, user_id)):
        return await message.reply(f"User {user.mention} is fbanned in {fed_name}. You have to unfban them before promoting.")
    keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Confirm', callback_data=f'promote_{user_id}_{owner_id}'),InlineKeyboardButton(text='Cancel', callback_data=f'cancel_{user_id}_{owner_id}')]])
    await message.reply(f"Please get {user.mention} to confirm that they would like to be fed admin for {fed_name}.",reply_markup=keyboard)


@app.on_message(filters.command("fban"))
async def fed_ban(client, message):
    chat_id = message.chat.id
    userID = await extract_user(message)
    bannerMention = message.from_user.mention 
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id
    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    get_user = await app.get_users(user_ids=userID)
    FED_ADMINS = get_fed_admins(fed_id)
    if userID == BOT_ID:
        return await message.reply( " I am not going to fban myself.")
    if bannedID not in FED_ADMINS:
        return await message.reply(f"You aren't a federation admin of {fed_name}.")
    if (message.reply_to_message and len(message.command) >= 2):
        reason_text = ' '.join(message.text.split()[1:])   
    elif (len(message.command) >= 3):
        reason_text = ' '.join(message.text.split()[2:])  
    else:
        reason_text = 'No reason was given'
    reason = f"{reason_text} // Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        old_reason = get_fed_reason(fed_id, userID)
        if not old_reason == reason:
            update_reason(fed_id, userID, reason)
            fed_message = (
            f'**This user was already banned in the** "{fed_name}" **federation, I\'ll update the reason:**\n\n'
            f"Fed Administrator: {bannerMention}\n"
            f"User: {get_user.mention}\n"
            f"User ID: `{userID}`\n"
            f"Old Reason: `{old_reason}`\n"
            f"Updated Reason: `{reason}`"
        )
        else:
            fed_message = (f"User {get_user.mention} has already been fbanned, with the exact same reason.")
    else:
        user_fban(fed_id, userID, reason)
        connected_chats = get_connected_chats(fed_id)
        BannedChats = []
        for chat_id in connected_chats:
            GetData = await app.get_chat_member(chat_id=chat_id,user_id=BOT_ID)
            if GetData['can_restrict_members']:
                if await app.chat.ban_member(chat_id,userID):
                    BannedChats.append(chat_id)
            else:
                continue
        fed_message = (
                f'**New Federation Ban in the** "{fed_name}" **federation:**\n\n'
                f"Fed Administrator: {bannerMention}\n"
                f"User: {get_user.mention}\n"
                f"User ID: `{userID}`\n"
                f"Reason: {reason}\n"
                f"Affected Chats: `{len(BannedChats)}`"
            )
    await message.reply(fed_message)

@app.on_message(filters.command("unfban"))
async def unfed_ban(client, message):
    chat_id = message.chat.id
    userID = await extract_user(message)
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id
    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    FED_ADMINS = get_fed_admins(fed_id)
    if userID == BOT_ID:
        return await message.reply("How do you think I would've fbanned myself that you are trying to unfban me? Never seen such retardedness ever before.")
    if bannedID not in FED_ADMINS:
        return await message.reply(f"You aren't a federation admin of {fed_name}.")
    if (message.reply_to_message and len(message.command) >= 2):
        reason_text = ' '.join(message.text.split()[1:])   
    elif (len(message.command) >= 3):
        reason_text = ' '.join(message.text.split()[2:])  
    else:
        reason_text = 'No reason was given'
    reason = f"{reason_text} // un-Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        user_unfban(fed_id, userID)

@app.on_message(filters.command("renamefed"))
async def Rename_fed(client, message):
    owner_id = message.from_user.id
    if message.chat.type != 'private':
        return await message.reply("You can only rename your fed in PM.")
    if len(message.command) < 2:
        return await message.reply("You need to give your federation a name! Federation names can be up to 64 characters long.")
    if (len(' '.join(message.command[1:])) > 60 ):
        return await message.reply(
            "Your fed must be smaller than 60 words."
        )
    fed_id = get_fed_from_ownerid(owner_id)
    if fed_id is None:
        return await message.reply("It doesn't look like you have a federation yet!")
    fed_name = ' '.join(message.command[1:])
    old_fed_name = get_fed_name(owner_id=owner_id)
    fed_rename_db(owner_id, fed_name)
    await message.reply(f"I've renamed your federation from '{old_fed_name}' to '{fed_name}'. ( FedID: `{fed_id}`.)")
    connected_chats = get_connected_chats(fed_id)
    for chat_id in connected_chats:
        await app.send_message(
            chat_id=chat_id,text=(
                "**Federation renamed**\n"
                f"**Old fed name:** {old_fed_name}\n"
                f"**New fed name:** {fed_name}\n"
                f"FedID: `{fed_id}`"))

__MODULE__ = Federations
__HELP__ = """
Everything is fun, until a spammer starts entering your group, and you have to block it. Then you need to start banning more, and more, and it hurts.
But then you have many groups, and you don't want this spammer to be in one of your groups - how can you deal? Do you have to manually block it, in all your groups?

**No longer!** With Federation, you can make a ban in one chat overlap with all other chats.

You can even designate federation admins, so your trusted admin can ban all the spammers from chats you want to protect.

**Commands:**
- /newfed <fedname>: create a new Federation with the name given. Users are only allowed to have one Federation. This method can also be used to rename the Federation. (max. 64 characters)
- /joinfed <FedID>: join the current chat to the Federation. Only chat owners can do this. Every chat can only be in one Federation.
- /fedpromote <user>: promote Users to give fed admin. Fed owner only.
- /fban <user>: ban users from all federations where this chat takes place, and executors have control over.
- /unfban <user>: cancel User from all federations where this chat takes place, and that the executor has control over.
- /renamefed : rename your  Federation.
- /leavefed: Leaves current chat from the fed.
- /fedinfo : get fed informations.
"""