from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.lang import *


fbuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("« Back", callback_data='startcq')
        ]]
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="English🇬🇧", callback_data="languages_en"
            ),
            InlineKeyboardButton(
                text="සිංහල🇱🇰", callback_data="languages_si"
            )
        ],
        [
            InlineKeyboardButton(
                text="हिन्दी🇮🇳", callback_data="languages_hi"
            ),
            InlineKeyboardButton(
                text="Tamil🇮🇳", callback_data="languages_ta"
            )
        ],
        [
            InlineKeyboardButton(
                text="मराठी 🇮🇳", callback_data="languages_ma"
            ),
            InlineKeyboardButton(
                text="తెలుగు 🇮🇳", callback_data="languages_ta"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌎 Help us with translation 🌎",
                url=f"https://crwd.in/szrosebot",
            )
        ],
        [
            InlineKeyboardButton(
                text="Close ✖️", callback_data="close_data"
            ),
        ],
    ]
)

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    user = CallbackQuery.message.from_user.mention
    await app.send_message(
        CallbackQuery.message.chat.id,
        text= _["setting_1"].format(user),
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

