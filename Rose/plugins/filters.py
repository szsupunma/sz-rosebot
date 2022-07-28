import io
from re import escape as re_escape
from secrets import choice
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from Rose import app,LOG_GROUP_ID
from Rose.mongo.filterdb import Filters
from Rose.utils.cmd_senders import send_cmd
from Rose.utils.custom_filters import command, owner_filter
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.msg_types import Types, get_filter_type
from Rose.utils.regex_utils import regex_searcher
from Rose.utils.string import (
    build_keyboard,
    escape_mentions_using_curly_brackets,
    parse_button,
    split_quotes,
)
from pyrogram import filters
from Rose.mongo.connectiondb import active_connection
from lang import get_command
from Rose.utils.lang import language
from Rose.utils.filter_groups import chat_filters_group
from Rose.plugins.fsub import ForceSub
from button import Filter

db = Filters()

FILTERS = get_command("FILTERS")
ADD = get_command("ADDFILTER")
STOP = get_command("STOPFILTER")
RMALLFILTERS = get_command("RMALLFILTERS")

@app.on_message(filters.command(FILTERS) & filters.incoming)
@language
async def view_filters(client, message: Message, _):
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    chat_type = message.chat.type
    userid = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if not userid:
        return await message.reply(_["connection1"].format(chat_id))
    if chat_type == "private":
        userid = message.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is None:
            return await message.reply_text(_["filter2"])
        grp_id = grpid
        try:
            chat = await client.get_chat(grpid)
            title = chat.title
        except:
            return await message.reply_text(_["filter1"])
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in ["administrator", "creator"]:
        return
    texts = db.get_all_filters(grp_id)
    if texts:
        filterlist = f"**Total number of filters in** {title} \n\n"
        for text in texts:
            keywords = f"•`{text}`\n"
            filterlist += keywords
        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "filter.txt"
                return await message.reply_document(document=keyword_file,quote=True)
    else:
        filterlist = f"There are no active filters in **{title}**"
    await message.reply_text(text=filterlist,quote=True,parse_mode="md")

@app.on_message(filters.command(ADD) & filters.incoming)
@language
async def addfilter(client, message: Message, _):
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    chat_type = message.chat.type
    userid = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if not userid:
        return await message.reply(_["connection1"].format(chat_id))
    if chat_type == "private":
        userid = message.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is None:
            return await message.reply_text(_["filter2"])
        grp_id = grpid
        try:
            chat = await client.get_chat(grpid)
            title = chat.title
        except:
            return await message.reply_text(_["filter1"])
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in ["administrator", "creator"]:
        return
    args = message.command
    if len(args) < 2:
        return await message.reply_text(_["filter3"])
    all_filters = db.get_all_filters(grp_id)
    actual_filters = {j for i in all_filters for j in i.split("|")}
    if (len(all_filters) >= 100) and (len(actual_filters) >= 50):
        return await message.reply_text(_["filter4"])
    if not message.reply_to_message and len(message.text.split()) < 3:
        return await message.reply_text(_["filter5"])
    if message.reply_to_message and len(args) < 2:
        return await message.reply_text(_["filter5"])
    extracted = await split_quotes(args[1])
    keyword = extracted[0].lower()
    for k in keyword.split("|"):
        if k in actual_filters:
            return await message.reply_text(_["filter6"].format(k))
    if not keyword:
        return await message.reply_text(f"<code>{message.text}</code>\n\nError: You must give a name for this Filter!",)
    if keyword.startswith("<") or keyword.startswith(">"):
        return await message.reply_text(_["filter7"])
    eee, msgtype, file_id = await get_filter_type(message)
    lol = eee if message.reply_to_message else extracted[1]
    teks = lol if msgtype == Types.TEXT else eee
    if not message.reply_to_message and msgtype == Types.TEXT and len(message.text.split()) < 3:
        return await message.reply_text(_["filter8"])
    if not teks and not msgtype:
        return await message.reply_text(_["filter9"])
    if not msgtype:
        return await message.reply_text(_["filter10"])
    add = db.save_filter(grp_id, keyword, teks, msgtype, file_id)
    if add:
        await message.reply_text(f"Saved filter for '<code>{', '.join(keyword.split('|'))}</code>' in <b>{title}</b>!",)
    await message.stop_propagation()


@app.on_message(filters.command(STOP) & filters.incoming )
@language
async def stop_filter(client, message: Message, _):
    chat_type = message.chat.type
    userid = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if not userid:
        return await message.reply(_["connection1"].format(chat_id))
    if chat_type == "private":
        userid = message.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is None:
            return await message.reply_text(_["filter2"])
        grp_id = grpid
        try:
            chat = await client.get_chat(grpid)
            title = chat.title
        except:
            return await message.reply_text(_["filter1"])
    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in ["administrator", "creator"]:
        return
    args = message.command
    if len(args) < 1:
        return await message.reply_text(_["filter11"])
    chat_filters = db.get_all_filters(grp_id)
    act_filters = {j for i in chat_filters for j in i.split("|")}
    if not chat_filters:
        return await message.reply_text(_["filter12"])
    for keyword in act_filters:
        if keyword == message.text.split(None, 1)[1].lower():
            db.rm_filter(grp_id, message.text.split(None, 1)[1].lower())
            await message.reply_text(_["filter13"])
            await message.stop_propagation()
    await message.reply_text(_["filter14"])
    await message.stop_propagation()

@app.on_message(command(RMALLFILTERS))
async def rm_allfilters(_, m: Message):
    st = await _.get_chat_member(m.chat.id, m.from_user.id)
    if (st.status != "creator"):
        return
    all_bls = db.get_all_filters(m.chat.id)
    if not all_bls:
        return await m.reply_text("No filters to stop in this chat.")
    return await m.reply_text("Are you sure you want to clear all filters?",reply_markup=ikb([[("⚠️ Confirm", "rm_allfilters"), ("❌ Cancel", "close_admin")]]))



async def send_filter_reply(c: app, m: Message, trigger: str):
    getfilter = db.get_filter(m.chat.id, trigger)
    if m and not m.from_user:
        return
    if not getfilter:
        return await m.reply_text("Cannot find a type for this filter!!",quote=True)
    msgtype = getfilter["msgtype"]
    if not msgtype:
        return await m.reply_text("Cannot find a type for this filter!!")
    try:
        splitter = "%%%"
        filter_reply = getfilter["filter_reply"].split(splitter)
        filter_reply = choice(filter_reply)
    except KeyError:
        filter_reply = ""
    parse_words = [
        "first",
        "last",
        "fullname",
        "id",
        "mention",
        "username",
        "chatname",
    ]
    text = await escape_mentions_using_curly_brackets(m, filter_reply, parse_words)
    teks, button = await parse_button(text)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    textt = teks
    try:
        if msgtype == Types.TEXT:
            if not button:
                return await m.reply_text(textt,quote=True,disable_web_page_preview=True)
            try:
                return await m.reply_text(textt,reply_markup=button,disable_web_page_preview=True,quote=True)
            except RPCError as ef:
                return await m.reply_text("An error has occured! Cannot parse filters.",quote=True)
        elif msgtype in (Types.STICKER,Types.VIDEO_NOTE,Types.CONTACT,Types.ANIMATED_STICKER,):
            await (await send_cmd(c, msgtype))(m.chat.id,getfilter["fileid"],reply_markup=button,reply_to_message_id=m.message_id,)
        else:
            await (await send_cmd(c, msgtype))(m.chat.id,getfilter["fileid"],caption=textt,reply_markup=button,reply_to_message_id=m.message_id,)
    except Exception as ef:
        await app.send_message(LOG_GROUP_ID,text= f"{ef}")
        return msgtype
    return msgtype


@app.on_message(filters.text & filters.group & ~filters.bot, group=chat_filters_group)
async def filters_watcher(c: app, m: Message):
    chat_filters = db.get_all_filters(m.chat.id)
    actual_filters = {j for i in chat_filters for j in i.split("|")}
    for trigger in actual_filters:
        pattern = r"( |^|[^\w])" + re_escape(trigger) + r"( |$|[^\w])"
        match = await regex_searcher(pattern, m.text.lower())
        if match:
            try:
                await send_filter_reply(c, m, trigger)
            except Exception as ef:
                await app.send_message(LOG_GROUP_ID,text= f"{ef}")
            break
        continue
    return




__MODULE__ = Filter
__HELP__ = """
Make your chat more lively with filters; The bot will reply to certain words!
Filters are case insensitive; every time someone says your trigger words, Rose will reply something else! can be used to create your own commands, if desired.

**Commands:**
- /filter <trigger> <reply>: Every time someone says "trigger", the bot will reply with "sentence". For multiple word filters, quote the trigger.
- /filters: List all chat filters.
- /stop <trigger>: Stop the bot from replying to "trigger".
- /stopall: Stop ALL filters in the current chat. This cannot be undone.

**Example:**

- Set a filter:
> ` /filter hello ` reply some message like : Hello there! How are you?
"""
__helpbtns__ = (
        [[
        InlineKeyboardButton('Markdown ', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Filters', callback_data="_random")
        ]]
)
