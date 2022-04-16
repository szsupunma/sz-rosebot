from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

supunma = """
**Basic Locktypes available for a chat: **
video
audio
document
forward
photo
sticker
gif
games
album
voice
video_note
contact
location
address
reply
message
comment
edit
mention
inline
polls
dice
buttons
media
email
url
bots
all
spoiler
spam
porn
anonchannel
Rose will delete user's message if locked content is sent
"""

@app.on_callback_query(filters.regex("_ucd"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunma,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

asuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    " Lock Types", callback_data="_ucd"
                ),            
            InlineKeyboardButton
                (
                    "Permissions Locks", callback_data="_kcd"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "Examples", callback_data="_lcd"
                )
        ],
        [
            InlineKeyboardButton('« Back', callback_data='bot_commands')
        ]]
)

supunm = """
**Permissions Locks Available for a chat:**
send_messages
send_stickers
send_gifs
send_media
send_games
send_inline
url_prev
send_polls
change_info
invite_user
pin_messages
all_permissions
"""
@app.on_callback_query(filters.regex("_kcd"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunm,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

supunmas = """
**Examples:**
- Lock stickers with:
> /lock sticker
- You can lock/unlock multiple items by chaining them:
> /lock sticker photo gif video
"""

@app.on_callback_query(filters.regex("_lcd"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunmas,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
