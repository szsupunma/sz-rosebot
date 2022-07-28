from secrets import choice
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, Message
from Rose import app
from Rose.mongo.notesdb import Notes, NotesSettings
from Rose.utils.cmd_senders import send_cmd
from Rose.utils.custom_filters import admin_filter, command, owner_filter
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.msg_types import Types, get_note_type
from Rose.utils.string import (
                                build_keyboard,
                                escape_mentions_using_curly_brackets,
                                parse_button,
)
from Rose.mongo.connectiondb import active_connection
from lang import get_command
from button import Note

SAVE = get_command("SAVE")
GET = get_command("GET")
PNOTES = get_command("PNOTES")
NOTES = get_command("NOTES")
CLEAR = get_command("CLEAR")
CLEARALL = get_command("CLEARALL")

db = Notes()
db_settings = NotesSettings()


@app.on_message(command(SAVE) & admin_filter & ~filters.bot)
async def save_note(_, m: Message):
    chat_type = m.chat.type
    userid = m.from_user.id if m.from_user else None
    if not userid:
        return await m.reply(f"You are anonymous admin. Use `/connect {m.chat.id}` in PM")
    if chat_type == "private":
        userid = m.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is None:
            return await m.reply_text("I'm not connected to any groups!")
        grp_id = grpid
        try:
            chat = await app.get_chat(grpid)
            title = chat.title
        except:
            return await m.reply_text("Make sure I'm present in your group!!")
    elif chat_type in ["group", "supergroup"]:
        grp_id = m.chat.id
        title = m.chat.title
    else:
        return
    adminx = await app.get_chat_member(grp_id, userid)
    if adminx.status not in ["administrator", "creator"]:
        return
    existing_notes = {i[0] for i in db.get_all_notes(grp_id)}
    name, text, data_type, content = await get_note_type(m)
    total_notes = db.get_all_notes(grp_id)
    if len(total_notes) >= 100:
        return await m.reply_text("Only 1000 Notes are allowed per chat!\nTo add more Notes, remove the existing one.")
    if not name:
        return await m.reply_text(f"<code>{m.text}</code>\n\nYou must give a name for this note!")
    note_name = name.lower()
    if note_name in existing_notes:
        return await m.reply_text(f"This note {note_name} already exists! In this chat")
    if not m.reply_to_message and data_type == Types.TEXT and len(m.text.split()) < 3:
        return await m.reply_text(f"<code>{m.text}</code>\n\nThere is no text in here!")
    if not data_type:
        return await m.reply_text(f"<code>{m.text}</code>\n\nError: There is no data in here!")
    db.save_note(grp_id, note_name, text, data_type, content)
    return await m.reply_text(f"Saved note <code>{note_name}</code>!\nGet it with <code>/get {note_name}</code> or <code>#{note_name}</code>")
    


async def get_note_func(c: app, m: Message, note_name, priv_notes_status):
    reply_text = m.reply_to_message.reply_text if m.reply_to_message else m.reply_text
    reply_msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id
    if m and not m.from_user:
        return
    if priv_notes_status:
        note_hash = next(i[1] for i in db.get_all_notes(m.chat.id) if i[0] == note_name)
        return await reply_text(
            f"Click on the button to get the note <code>{note_name}</code>",
            reply_markup=ikb([[("Click Me!",f"https://t.me/szRosebot?start=note_{m.chat.id}_{note_hash}","url")]]))
    getnotes = db.get_note(m.chat.id, note_name)
    msgtype = getnotes["msgtype"]
    if not msgtype:
        return await reply_text("Cannot find a type for this note!!")
    try:
        splitter = "%%%"
        note_reply = getnotes["note_value"].split(splitter)
        note_reply = choice(note_reply)
    except KeyError:
        note_reply = ""
    parse_words = [
        "first",
        "last",
        "fullname",
        "id",
        "username",
        "mention",
        "chatname",
    ]
    text = await escape_mentions_using_curly_brackets(m, note_reply, parse_words)
    teks, button = await parse_button(text)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    textt = teks
    try:
        if msgtype == Types.TEXT:
            if button:
                try:
                    return await reply_text(textt,reply_markup=button,disable_web_page_preview=True)
                except RPCError as ef:
                    print(ef)
                    return await reply_text("An error has occured! Cannot parse note.")
            else:
                return await reply_text(textt,quote=True,disable_web_page_preview=True)
        elif msgtype in (Types.STICKER,Types.VIDEO_NOTE,Types.CONTACT,Types.ANIMATED_STICKER):
            await (await send_cmd(c, msgtype))(m.chat.id,getnotes["fileid"],reply_markup=button,reply_to_message_id=reply_msg_id)
        elif button:
            try:
                return await (await send_cmd(c, msgtype))(m.chat.id,getnotes["fileid"],caption=textt,reply_markup=button,reply_to_message_id=reply_msg_id)
            except RPCError as ef:
                return await m.reply_text(textt,reply_markup=button,disable_web_page_preview=True,reply_to_message_id=reply_msg_id)
        else:
            await (await send_cmd(c, msgtype))(m.chat.id,getnotes["fileid"],caption=textt,reply_markup=button,reply_to_message_id=reply_msg_id)
    except Exception as e:
        await m.reply_text(f"Error in notes: {e}")
    return


async def get_raw_note(c: app, m: Message, note: str):
    all_notes = {i[0] for i in db.get_all_notes(m.chat.id)}
    if m and not m.from_user:
        return
    if note not in all_notes:
        return await m.reply_text("This note does not exists!")
    getnotes = db.get_note(m.chat.id, note)
    msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id
    msgtype = getnotes["msgtype"]
    if not getnotes:
        return await m.reply_text("<b>Error:</b> Cannot find a type for this note!!")
    if msgtype == Types.TEXT:
        teks = getnotes["note_value"]
        await m.reply_text(teks, parse_mode=None, reply_to_message_id=msg_id)
    elif msgtype in (Types.STICKER,Types.VIDEO_NOTE,Types.CONTACT,Types.ANIMATED_STICKER,):
        await (await send_cmd(c, msgtype))(m.chat.id,getnotes["fileid"],reply_to_message_id=msg_id)
    else:
        teks = getnotes["note_value"] or ""
        await (await send_cmd(c, msgtype))(m.chat.id,getnotes["fileid"],caption=teks,reply_to_message_id=msg_id)
    return


@app.on_message(filters.regex(r"^#[^\s]+") & filters.group & ~filters.bot)
async def hash_get(c: app, m: Message):
    try:
        note = (m.text[1:]).lower()
    except TypeError:
        return
    all_notes = {i[0] for i in db.get_all_notes(m.chat.id)}
    if note not in all_notes:
        return
    priv_notes_status = db_settings.get_privatenotes(m.chat.id)
    return await get_note_func(c, m, note, priv_notes_status)
    


@app.on_message(command(GET) & filters.group & ~filters.bot)
async def get_note(c: app, m: Message):
    if len(m.text.split()) == 2:
        priv_notes_status = db_settings.get_privatenotes(m.chat.id)
        note = ((m.text.split())[1]).lower()
        all_notes = {i[0] for i in db.get_all_notes(m.chat.id)}
        if note not in all_notes:
            return await m.reply_text("This note does not exists!")
        await get_note_func(c, m, note, priv_notes_status)
    elif len(m.text.split()) == 3 and (m.text.split())[2] in ["noformat", "raw"]:
        note = ((m.text.split())[1]).lower()
        await get_raw_note(c, m, note)
    else:
        return await m.reply_text("Give me a note tag!")
    return


@app.on_message(command(NOTES) & filters.group & ~filters.bot)
async def local_notes(_, m: Message):
    chat_type = m.chat.type
    userid = m.from_user.id if m.from_user else None
    if not userid:
        return await m.reply(f"You are anonymous admin. Use `/connect {m.chat.id}` in PM")
    if chat_type == "private":
        userid = m.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is None:
            return await m.reply_text("I'm not connected to any groups!")
        grp_id = grpid
        try:
            chat = await app.get_chat(grpid)
            title = chat.title
        except:
            return await m.reply_text("Make sure I'm present in your group!!")
    elif chat_type in ["group", "supergroup"]:
        grp_id = m.chat.id
        title = m.chat.title
    else:
        return
    stf = await app.get_chat_member(grp_id, userid)
    if stf.status not in ["administrator", "creator"]:
        return
    getnotes = db.get_all_notes(grp_id)
    if not getnotes:
        return await m.reply_text(f"There are no notes in <b>{title}</b>.")
    msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id
    curr_pref = db_settings.get_privatenotes(grp_id)
    if curr_pref:
        pm_kb = ikb([[("All Notes",f"https://t.me/szRosebot?start=notes_{grp_id}","url")]])
        return await m.reply_text("Click on the button below to get notes!",reply_markup=pm_kb)
    rply = f"Notes in <b>{title}</b>:\n"
    for x in getnotes:
        rply += f"- <code>#{x[0]}</code>\n"
    rply += "\nYou can get a note by #notename or <code>/get notename</code>"
    return await m.reply_text(rply, reply_to_message_id=msg_id)
    
@app.on_message(command(CLEAR) & admin_filter & ~filters.bot)
async def clear_note(_, m: Message):
    if len(m.text.split()) <= 1:
        return await m.reply_text("What do you want to clear?")
    note = m.text.split()[1].lower()
    getnote = db.rm_note(m.chat.id, note)
    if not getnote:
        return await m.reply_text("This note does not exist!")
    return await m.reply_text(f"Note '`{note}`' deleted!")
    
@app.on_message(command(CLEARALL) & owner_filter & ~filters.bot)
async def clear_allnote(_, m: Message):
    all_notes = {i[0] for i in db.get_all_notes(m.chat.id)}
    if not all_notes:
        return await m.reply_text("No notes are there in this chat")
    return await m.reply_text("Are you sure you want to clear all notes?",reply_markup=ikb([[("⚠️ Confirm", "clear_notes"), ("❌ Cancel", "close_admin")]]))
    



__MODULE__ = Note
__HELP__ = """
Save data for future users with notes!
Notes are great to save random tidbits of information; a phone number, a nice gif, a funny picture - anything!

**User commands:**
- /get `<notename>`: Get a note.
- #notename: Same as `/get`.

**Admin commands:**
- /save `<notename>` `<note text>`: Save a new note called "word". Replying to a message will save that message. Even works on media!
- /clear `<notename>`: Delete the associated note.
- /notes: List all notes in the current chat.
- /saved: Same as /notes.
- /clearall: Delete ALL notes in a chat. This cannot be undone.
"""
