

from Rose import app
from pyrogram import emoji
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
)

lengths = 200

IMG = "https://telegra.ph/file/8bb5ad38249514dbf72e6.jpg"

@app.on_inline_query()
async def wishper_ai(_, sz: InlineQuery):
    query = sz.query
    split = query.split(' ', 1)
    if query == '' or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        title = "🔐 Write a whisper message"
        content = ("**Send whisper messages through inline mode**\n\n"
                   "Usage: `@szrosebot [@username] text`")
        description = "Usage: @szrosebot [@username] text"
        button = InlineKeyboardButton(
            "More-Help",
            url="https://t.me/szrosebot?start=learn"
        )

    elif not query.startswith('@'):
        title = f"{emoji.EYE} Whisper once to the first one who open it"
        content = (
            f"{emoji.EYE} The first one who open the whisper can read it"
        )
        description = f"{emoji.SHUSHING_FACE} {query}"
        button = InlineKeyboardButton(
            "🎯 show message",
            callback_data="show_whisper"
        )

    else:
        u_target = 'anyone' if (x := split[0]) == '@' else x
        title = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        content = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        description = f"{emoji.SHUSHING_FACE} {split[1]}"
        button = InlineKeyboardButton(
            f"{emoji.LOCKED_WITH_KEY} show message",
            callback_data="show_whisper"
        )

    switch_pm_text = f"{emoji.INFORMATION} Learn how to send whispers"
    switch_pm_parameter = "learn"

    await sz.answer(
        results=[
            InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(content),
                description=description,
                thumb_url=IMG,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        ],
        switch_pm_text=switch_pm_text,
        switch_pm_parameter=switch_pm_parameter
    )



__MODULE__ = "whisper"
__HELP__ = """
the other way to use me is to write the inline query by your self
the format should be in this arrangement

@szrosebot your whisper @username

now I'll split out the format in 3 parts and explain every part of it

1- @szrosebot
this is my username it should be at the beginning of the inline query so I'll know that you are using me and not another bot.

2- whisper message
it is the whisper that will be sent to the target user, you need to remove your whisper and insert your actual whisper.

3- @username
you should replace this with target's username so the bot will know that the user with this username can see your whisper message.

example:- 
@szrosebot hello this is a test @supunma

📎 the bot works in groups and the target user should be in the same group with you
what you are waiting for?!
try me now 😉 """

