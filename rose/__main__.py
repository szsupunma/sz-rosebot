"""
Copyright (c) 2021 TheHamkerCat
This is part of @szrosebot so don't change anything....
"""
    



import asyncio
import importlib
import re
import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pykeyboard import InlineKeyboard
from rose import (BOT_NAME, BOT_USERNAME, LOG_GROUP_ID,
                 aiohttpsession, app, app2)
from rose.modules import ALL_MODULES
from rose.adv import ADV_MODULES
from rose.base import BASE_MODULES
from rose.fun import FUN_MODULES
from rose.utils import paginate_modules
from rose.utils.dbfunctions import clean_restart_stage
from rose import LOGGER
from rose.utils.dbfunctions import  get_served_chats, get_served_users
from rose.utils.dbfunctions import get_gbans_count,get_served_chats,get_served_users                    
import pytz
import datetime
from pyrogram import filters
from rose.utils.dbfunctions import  get_served_chats, get_served_users     
import os
from pyrogram import filters
from rose import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pytz
import datetime
from rose.modules import ALL_MODULES
from pyrogram.errors import UserAlreadyParticipant
from rose import ForceSub
loop = asyncio.get_event_loop()

MARKDOWN = """
Commands Menu > Basic Menu > Notes
"""
HELPABLE = {}
IMPORTED = {}
BASICCMDS = {}
FUNTOOLS = {}
ADVTOOLS = {}
HELP_COMMANDS = {}  # For help menu

async def start_bot():
    global HELPABLE
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("rose.modules." + module_name)
        if not hasattr(imported_module, "__MODULE__"):
            imported_module.__MODULE__ = imported_module.__name__
        if not imported_module.__MODULE__.lower() in IMPORTED:
            IMPORTED[imported_module.__MODULE__.lower()] = imported_module
        else:
            raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELPABLE[imported_module.__MODULE__.lower()] = imported_module   
#new
            plugin_name = imported_module.__MODULE__.lower()
            plugin_dict_name = f"plugins.{plugin_name}.main"
        HELP_COMMANDS[plugin_dict_name] = {
            "buttons": [],
            "__MODULE__": [],
            "plug_cmds": [],
            "__HELP__": f"modules.{plugin_name}.help",
        }      
        if hasattr(imported_module, "__buttons__"):
           HELP_COMMANDS[plugin_dict_name]["buttons"] = imported_module.__buttons__    
        if hasattr(imported_module, "__plug_name__"):
            HELP_COMMANDS[plugin_dict_name]["plug_cmds"] = imported_module.__alt_name__

#new end   
    for module_name in ADV_MODULES:
        imported_adv = importlib.import_module("rose.adv." + module_name)
        # imported_adv = importlib.import_module("rose.adv." + module_name)
        if hasattr(imported_adv, "__advtools__") and imported_adv.__advtools__:
            ADVTOOLS[imported_adv.__MODULE__.lower()] = imported_adv
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELPABLE[imported_module.__MODULE__.lower()] = imported_module          
    for module_name in BASE_MODULES:
        imported_base = importlib.import_module("rose.base." + module_name)
        # imported_base = importlib.import_module("rose.base." + module_name)
        if hasattr(imported_base, "__basic_cmds__") and imported_base.__basic_cmds__:
            BASICCMDS[imported_base.__MODULE__.lower()] = imported_base
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELPABLE[imported_module.__MODULE__.lower()] = imported_module      
    for module_name in FUN_MODULES:
        imported_fun = importlib.import_module("rose.fun." + module_name)
        # imported_fun = importlib.import_module("rose.fun." + module_name)
        if hasattr(imported_fun, "__funtools__") and imported_fun.__funtools__:
            FUNTOOLS[imported_fun.__MODULE__.lower()] = imported_fun
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELPABLE[imported_module.__MODULE__.lower()] = imported_module              
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    restart_data = await clean_restart_stage()

    try:
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot started! Successfully")
    except Exception:
        pass
    try:
            await app2.join_chat("szteambots")
            await app2.join_chat("slbotzone")
    except UserAlreadyParticipant:
        pass
    await idle()
    await aiohttpsession.close()
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()
        

start_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="❓ Commands Menu ❓", callback_data="bot_commands"
            ),
        ],
        [
           InlineKeyboardButton(
                text="💫 Support", url="https://t.me/Darkenbotsupport"
            ),
            InlineKeyboardButton(
                text="👨‍💻Developer", url="http://t.me/Oshebrosl1"
            ),
        ],
        [
            InlineKeyboardButton(
                text="➕ Add Me To Your Group ➕",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

start_text = f"""
Hello There ! I'm **GhostBot** 👻
An  advanced telegram Group management Bot For help 
You Protect Your Groups & Suit For All Your Needs.
"""

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Help Commands ❓",
                url=f"t.me/{BOT_USERNAME}?start=help",
            )
        ]
    ]
)


basichelp_string = """
**👥Basic Group Commands**
✘ Base commands are the basic tools of Rose Bot which help you to manage 
your group easily and effectivelyYou can choose 
an option below, by clicking a button.
Also you can ask anything in [Support Group](https://t.me/Darkenbotsupport).

>> [Shorter the Way, Faster you Go! 🏃‍♂️](https://t.me/Darkenbotsteam)
"""

funtools_string = """
👨🏻‍💼**Expert**

✘ Extra tools which are available in bot and tools made for fun are here
You can choose an option below, by clicking a button.
Also you can ask anything in [Support Group](https://t.me/Darkenbotsupport).

Click buttons to get help [?](https://t.me/Darkenbotsteam)
"""

advtools_string = """


✘ Advanced commands will help you to secure your groups 
from attackers and do many stuff in group from a single bot
You can choose an option below, by clicking a button.
Also you can ask anything in [Support Group](https://t.me/Darkenbotsupport).

>> [Shorter the Way, Faster you Go! 🏃‍♂️](https://t.me/Darkenbotsteam)
"""

@app.on_message(filters.command(["start", f"@{BOT_USERNAME}"]))
async def start(_, message):
    FSub = await ForceSub(_, message)
    if FSub == 400:
        return
    Time_Zone = "Asia/Kolkata"
    zone = datetime.datetime.now(pytz.timezone(f"{Time_Zone}"))  
    timer = zone.strftime("%I:%M %p")
    dater = zone.strftime("%b %d")   
    await app.send_message(
                LOG_GROUP_ID,
                f"""
#NEW_USER
username- {message.from_user.mention}
userid- `{message.from_user.id}`
started time - `2022 {dater}:{timer} `         
                """
            )
    if message.chat.type != "private":
        total=await app.get_chat_members_count(message.chat.id)
        await app.send_message(
                LOG_GROUP_ID,
                f"""
#NEW_GROUP
Total users in group - {total}
started time - `2022 {dater}:{timer} `         
                """
            )
        return await message.reply(
            "**Heya, @szrosebot here :) PM me if you have any questions how to use me!**", reply_markup=keyboard
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"**{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply(
            start_text,
            reply_markup=start_button,
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="start PM",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Click on the below button to get help about `{name}`",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "**PM me if you have any questions how to use me!**", reply_markup=keyboard
                )
        else:
            await message.reply(
                "**PM me if you have any questions how to use me!**", reply_markup=keyboard
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                text = (
                    f"**{HELPABLE[name].__MODULE__}**:\n"
                    + HELPABLE[name].__HELP__
                )
                await message.reply(text, disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    text,
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True,
                )
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )
    return


keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👮‍♀️Basic Menu", callback_data="basic_menu"
                        ),
                        InlineKeyboardButton(
                            text="👨‍🔧 Advanced Menu", callback_data="adv_menu"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="👨🏻‍💼 Expert ", callback_data="ftools_back"
                        ),
                        InlineKeyboardButton(
                            text="🕵🏻‍♀️ Inline ", callback_data="_inline"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="👱‍♂️How to Use Me", callback_data="_how"
                        ),
                        InlineKeyboardButton(
                            text="👩‍💻About Me", callback_data="_about"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="News Channel 🗣", url="https://t.me/Darkenbotsteam"
                        ),
                        InlineKeyboardButton(
                            text="Support Group👥", url="https://t.me/Darkenbotsupport"
                        ),
                    ],
                    [
                        InlineKeyboardButton('📖 VC - player - Guides', callback_data="_vc")
                    ],

                        [InlineKeyboardButton(text="🔼Collapse", callback_data="bot_commands")],
                ]
            )

texts = """
**Welcome to help menu**
I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.
"""

@app.on_callback_query(filters.regex("expand_"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=texts,
        reply_markup=keyboar,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
async def help_parser(name, keyboard=None):
    if not keyboard:
         keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👮‍♀️Basic Menu", callback_data="basic_menu"
                        ),
                        InlineKeyboardButton(
                            text="👨‍🔧 Advanced Menu", callback_data="adv_menu"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="👨🏻‍💼 Expert ", callback_data="ftools_back"
                        ),
                        InlineKeyboardButton(
                            text="🕵🏻‍♀️ Inline ", callback_data="_inline"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔽 Expand Menu ", callback_data="expand_"
                        )
                    ],
                        [InlineKeyboardButton(text="🔙 Back", callback_data="startcq")],
                ]
            )


    return (
        """
**Welcome to help menu**

I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, query):
    text, keyboard = await help_parser(query.from_user.mention)
    await query.message.edit(
        text=text,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )

@app.on_callback_query(filters.regex("startcq"))
async def startcq(_, query):
    await query.message.edit(
            text=start_text,
            disable_web_page_preview=True,
            reply_markup=start_button)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
**Welcome to help menu**

I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.
 """
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = (
                "Here is the help for the **{}** module:".format(
                    HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__HELP__
            )
        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=start_text,
            reply_markup=start_button,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )
    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )
    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )
    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
    return await client.answer_callback_query(query.id)


@app.on_callback_query(filters.regex(r"ftools_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"ftools_module\((.+?)\)", query.data)
    prev_match = re.match(r"ftools_prev\((.+?)\)", query.data)
    next_match = re.match(r"ftools_next\((.+?)\)", query.data)
    back_match = re.match(r"ftools_back", query.data)
    if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the **{}** module:".format(
                    HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__funtools__
            )
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙 Back", callback_data="ftools_back")]]
                ),
            )
    elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=funtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, FUNTOOLS, "ftools")
                ),
            )
    elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_text(
                text=funtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, FUNTOOLS, "ftools")
                ),
            )
    elif back_match:
            await query.message.edit_text(
                text=funtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, FUNTOOLS, "ftools")
                ))

@app.on_callback_query(filters.regex(r"advt_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"advt_module\((.+?)\)", query.data)
    prev_match = re.match(r"advt_prev\((.+?)\)", query.data)
    next_match = re.match(r"advt_next\((.+?)\)", query.data)
    back_match = re.match(r"advt_back", query.data)
    if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the **{}** module:".format(
                    HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__advtools__
            )
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙 Back", callback_data="advt_back")]]
                ),
            )
    elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=advtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, ADVTOOLS, "advt")
                ),
            )
    elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_text(
                text=advtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, ADVTOOLS, "advt")
                ),
            )
    elif back_match:
            await query.message.edit_text(
                text=advtools_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, ADVTOOLS, "advt")
                ))

@app.on_callback_query(filters.regex(r"basict_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"basict_module\((.+?)\)", query.data)
    prev_match = re.match(r"basict_prev\((.+?)\)", query.data)
    next_match = re.match(r"basict_next\((.+?)\)", query.data)
    back_match = re.match(r"basict_back", query.data)
    if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the **{}** module:".format(
                    HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__basic_cmds__
            )
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙 Back", callback_data="basict_back")]]
                ),
            )
    elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=basichelp_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, BASICCMDS, "basict")
                ),
            )
    elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_text(
                text=basichelp_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, BASICCMDS, "basict")
                ),
            )
    elif back_match:
            await query.message.edit_text(
                text=basichelp_string,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, BASICCMDS, "basict")
                ))


UTTON_10 = InlineKeyboardMarkup(
        [
            InlineKeyboardButton(text="-Go Inline-", switch_inline_query_current_chat=""),
        ]
)


TEXT_PART_1 = """
Here is the help for the **Formatting** 
Rose supports a large number of formatting options 
to make your messages more expressive. Take a look 
by clicking the buttons below!
"""

BTTON_1 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Configuration', callback_data="next_0"),
        InlineKeyboardButton('Formatting ', callback_data='for_commands')
        ],
        [
        InlineKeyboardButton('Bug Report', url="https://t.me/slbotzone")
        ],
        [InlineKeyboardButton('🔙 Back', callback_data='bot_commands')
        ]]
  
)

BUTTON= InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Markdown  Formatting', callback_data="for_ommands"),
        InlineKeyboardButton('Fillings', callback_data='for_mmands')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="for_mands")
        ],
        [InlineKeyboardButton('🔙 Back', callback_data='bot_commands')
        ]]
  
)
@app.on_callback_query(filters.regex("for_commands"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART_1,
        reply_markup=BUTTON,
    )

    await CallbackQuery.message.delete()

TEXT_PART_20= """
<b>Markdown Formatting</b>
You can format your message using bold, italics, underline, and much more. Go ahead and experiment!
<b>Supported markdown:</b>
- <code>**Bold**</code> : This will show as <b>bold</b> text.
- <code>~strike~</code>: This will show as <strike>strike</strike> text.
- <code>__italic__</code>: This will show as <i>italic</i> text.
- <code>--underline--</code>: This will show as <u>underline</u> text.
- <code>`code words`</code>: This will show as <code>code</code> text.
- <code>||spoiler||</code>: This will show as <spoiler>Spoiler</spoiler> text.
- <code>[hyperlink](google.com)</code>: This will create a <a href='https://www.google.com'>hyperlink</a> text.
- [My Button](buttonurl://example.com): This is the formatting used for creating buttons. 

This example will create a button named "My button" which opens example.com when clicked.

<b>Note:</b> You can use both markdown & html tags.
If you would like to send buttons on the same row, use the :same formatting.

<b>Button formatting:</b>
Example:
```
[button 1](buttonurl:example.com)
[button 2](buttonurl://example.com:same)
[button 3](buttonurl://example.com)
```
This will show button 1 and 2 on the same line, with 3 underneath.
"""

BUTTON_20 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🔙 Back', callback_data="for_commands"),
        ]]
  
)

@app.on_callback_query(filters.regex("for_ommands"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART_20,
        reply_markup=BUTTON_20,
    )
    await CallbackQuery.message.delete()

TEXT_PART_30 = """
**Fillings**
You can also customise the contents of your message with contextual data. 
For example, you could mention a user by name in the welcome message, or mention them in a filter!
You can use these to mention a user in notes too!
**Supported fillings:**
- `{first}`: The user's first name.
- `{last}`: The user's last name.
- `{fullname}`: The user's full name.
- `{username}`: The user's username. If they don't have one, mentions the user instead.
- `{mention}`: Mentions the user with their firstname.
- `{id}`: The user's ID.
- `{chatname}`: The chat's name.
- `{rules}`: Adds Rules Button to Message.
"""

@app.on_callback_query(filters.regex("for_mmands"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART_30,
        reply_markup=BUTTON_20,
    )
    await CallbackQuery.message.delete()  

TEXT_PART_40 = """
**Random Content**
Another thing that can be fun, is to randomise the contents of a message. 
Make things a little more personal by changing welcome messages, or changing notes!
**How to use random contents:**
- %%%: This separator can be used to add  random replies to the bot.
**For example:**
`hello
%%%
how are you`
This will randomly choose between sending the first message, "hello", or the second message, "how are you".
Use this to make Rose feel a bit more customised! (only works in filters/notes)
**Example welcome message:**
- Every time a new user joins, they'll be presented with one of the three messages shown here.
-> /filter "hey"
hello there `{first}`!
%%%
Ooooh, `{first}` how are you?
%%%
Sup? `{first}`
"""

@app.on_callback_query(filters.regex("for_mands"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART_40,
        reply_markup=BUTTON_20,
    )
    await CallbackQuery.message.delete()      

@app.on_callback_query(filters.regex("format_commands"))
async def commands_callbacc(_, CallbackQuery):
    Time_Zone = "Asia/Kolkata"
    zone = datetime.datetime.now(pytz.timezone(f"{Time_Zone}"))  
    timer = zone.strftime("%I:%M %p")
    dater = zone.strftime("%b %d")    
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans = await get_gbans_count()
    modules_count = len(ALL_MODULES)

    TEXT_PART = f"""
@szrosebot ** is one of the fastest and most feature filled group manager**.   
 
 - **Latest Update Time** : `2022 {dater}:{timer}`
 - **Modules Loaded **:  `{modules_count}`
 - **Globally banned users.** :  `{gbans}`
@szrosebot **Mongo database stats**
 - ** Users ** : `{served_users}`
 - ** chats.** : `{served_chats}`

 
 **Why Rose**:
 
- **Simple**: `Easy usage and compaitble with many bot commands.`
- **Featured**: `Many features which other group management bots don't have.`
- **Fast:** `Guess what? It's not made using SQL, we use mong as our database.`
    """
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART,
        reply_markup=BTTON_1,
    )

    await CallbackQuery.message.delete()

TEXT_PART_1 = """
**Welcome to the Ghost Configuration**
The first thing to do is to add Ghost Bot ✨ to your group! 
For doing that, press the under button and select your group,
then press Done to continue the tutorial..
"""

TEXT_PART_2 = """
**Ok, well done!**
Now to let me work correctly, you need to make me Admin of your Group!
To do that, follow this easy steps:
▫️ Go to your group
▫️ Click Manage Group
▫️ Goto Administrators 
▫️ Press on Administrator
▫️ Add @szrosebot as Admin
▫️ Give full permissions 
▫️ Confirm
"""

TEXT_PART_3 = """
**Excellent!** Now the Bot is ready to use!
All commands can be used with / 
If you're facing any difficulties in setting up me in your group, 
so don't hesitate to come in @slbotzone.
We would love to help you.
"""


BUTTON_1 = InlineKeyboardMarkup(
        [[        
        InlineKeyboardButton('Add Rose to Chat ! 🎉', url='http://t.me/darkenghostbot?startgroup=new')
        ],
        [InlineKeyboardButton('Done ✅', callback_data="next_1")
        ]]
  
)

BUTTON_2 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Done ✅', callback_data="next_2"),
        ]]
  
)


BUTTON_3 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('✅Continue✅', callback_data="bot_commands"),
        ]]
  
)

@app.on_message(filters.command("tutorial") & ~filters.edited)
async def tutorial(client, message):  
  await message.reply(TEXT_PART_1, reply_markup=(BUTTON_1))

@app.on_callback_query(filters.regex(pattern=r"next_0"))
async def popat(_, CallbackQuery): 
  await CallbackQuery.edit_message_text(TEXT_PART_1, reply_markup=(BUTTON_1))  
  
@app.on_callback_query(filters.regex(pattern=r"next_1"))
async def popat(_, CallbackQuery): 
  await CallbackQuery.edit_message_text(TEXT_PART_2,reply_markup=(BUTTON_2))
  
@app.on_callback_query(filters.regex(pattern=r"next_2"))
async def popat(_, CallbackQuery): 
  await CallbackQuery.edit_message_text(TEXT_PART_3, reply_markup=(BUTTON_3))



text = """
@szrosebot is one of the fastest and most feature filled group manager.

Ghost ✨ is developed and actively maintained by @Darkenbotsteam!

Rose has been online since 2022/2/28 and have many [groups and users.](https://t.me/Darkenbotsteam)

**Why Rose:**
- **Simple**: Easy usage and compaitble with many bot commands.
- **Featured**: Many features which other group management bots don't have.
- **Fast**: Pyrogram base bot and use mongo as database.

**Current Version:** `1.0.6` | [Special Credits](https://telegra.ph/Special-Credits-02-02)
"""
@app.on_callback_query(filters.regex("_about"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


abuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="expand_"
                )
        ]
    ]
)

@app.on_callback_query(filters.regex("_how"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PAT_1,
        reply_markup=BUTON_1,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

TEXT_PAT_1 = """
**Welcome to the Rose Configuration**
The first thing to do is to add Ghost Bot ✨ to your group! 
For doing that, press the under button and select your group,
then press Done to continue the tutorial..
"""

TEXT_ART_2 = """
**Ok, well done!**
Now to let me work correctly, you need to make me Admin of your Group!
To do that, follow this easy steps:
▫️ Go to your group
▫️ Click Manage Group
▫️ Goto Administrators 
▫️ Press on Administrator
▫️ Add @szrosebot as Admin
▫️ Give full permissions 
▫️ Confirm
"""

TEXT_PART_3 = """
**Excellent!** Now the Bot is ready to use!
All commands can be used with / 
If you're facing any difficulties in setting up me in your group, 
so don't hesitate to come in @slbotzone.
We would love to help you.
"""


BUTON_1 = InlineKeyboardMarkup(
        [[        
        InlineKeyboardButton('Add Rose to Chat ! 🎉', url='http://t.me/darkenghostbot?startgroup=new')
        ],
        [InlineKeyboardButton('Done ✅', callback_data="next_100")
        ]]
  
)

BUTON_2 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Done ✅', callback_data="next_200"),
        ]]
  
)


BUTON_3 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('✅Continue✅', callback_data="bot_commands"),
        ]]
  
)

@app.on_callback_query(filters.regex("next_100"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_ART_2,
        reply_markup=BUTON_2,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("next_200"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=TEXT_PART_3,
        reply_markup=BUTON_3,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

keywords_list = [
    "image",
    "wall",
    "tmdb",
    "lyrics",
    "exec",
    "search",
    "ping",
    "tr",
    "ud",
    "info",
    "google",
    "torrent",
    "wiki",
    "music",
    "logo",
]
inline = """
**Click A Button To Get Started**
"""
@app.on_callback_query(filters.regex("_inline"))
async def commands_callbacc(_, CallbackQuery):
    buttons = InlineKeyboard(row_width=3)
    buttons.add(
        *[
            (InlineKeyboardButton(text=i, switch_inline_query_current_chat=i))
            for i in keywords_list
        ]
    )
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=inline,
        reply_markup=buttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
#app run is here
LOGGER.info("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Bot : Powerfull telegram Group management Bot ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
└───────────────────────────────────────────────┘ """)
LOGGER.info(f"Version: stable")
LOGGER.info(f"Owner: @supunma")

if __name__ == "__main__":
    uvloop.install()
    try:
        try:
            loop.run_until_complete(start_bot())
        except asyncio.exceptions.CancelledError:
            pass
        loop.run_until_complete(asyncio.sleep(3.0))  
    finally:
        loop.close()
