from pyrogram.types import Message
from Rose import *
from Rose.mongo.rulesdb import Rules



async def get_private_rules(_, m: Message, help_option: str):
    chat_id = int(help_option.split("_")[1])
    rules = Rules(chat_id).get_rules()
    if not rules:
        await m.reply_text(
            "The Admins of that group have not setup any rules!",
            quote=True,
        )
        return ""
    await m.reply_text(
        f"""
** Rules are**:

{rules}
""",
        quote=True,
        disable_web_page_preview=True,
    )
    return ""

async def get_learn(_, m: Message, help_option: str):
    await m.reply_text("""
the other way to use me is to write the inline query by your self
the format should be in this arrangement

`@szrosebot your whisper @username`

now I'll split out the format in 3 parts and explain every part of it

1- `@szrosebot`
this is my username it should be at the beginning of the inline query so I'll know that you are using me and not another bot.

2- `whisper message`
it is the whisper that will be sent to the target user, you need to remove your whisper and insert your actual whisper.

3- `@username`
you should replace this with target's username so the bot will know that the user with this username can see your whisper message.

example:- 
`@szrosebot hello this is a test @supunma`

📎 the bot works in groups and the target user should be in the same group with you
what you are waiting for?!
try me now 😉
""", quote=True, disable_web_page_preview=True)

    return ""


