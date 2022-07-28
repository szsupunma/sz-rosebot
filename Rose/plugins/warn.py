from time import time
from pyrogram import filters
from pyrogram.types import (
    ChatPermissions,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    Message)
from Rose.core.keyboard import ikb
from Rose import app, BOT_ID
from Rose.mongo.warnsdb import Warns, WarnSettings
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.custom_filters import admin_filter, command, restrict_filter
from Rose.utils.extract_user import extract_user
from Rose.utils.parser import mention_html
from Rose.utils.lang import language
from button import Warnin

@app.on_message(command(["warn", "swarn", "dwarn"]) & restrict_filter)
@language
async def warn(client, message: Message, _):  
    if message.reply_to_message:
        r_id = message.reply_to_message.message_id
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
        else:
            reason = None
    else:
        r_id = message.message_id
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]
        else:
            reason = None
    if not len(message.command) > 1 and not message.reply_to_message:
        await message.reply_text(_["warn1"])
        return

    user_id, user_first_name, _ = await extract_user(app, message)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="❗️ Un Mute",callback_data=f"_unwarn_{user_id}")]])
    if user_id == BOT_ID:
        await message.reply_text(_["warn2"])
        return
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(message, "warn_user"))}
    if user_id in admins_group:
        await message.reply_text(_["warn4"])
        return
    warn_db = Warns(message.chat.id)
    warn_settings_db = WarnSettings(message.chat.id)
    _, num = warn_db.warn_user(user_id, reason)
    warn_settings = warn_settings_db.get_warnings_settings()
    if num >= warn_settings["warn_limit"]:
        if warn_settings["warn_mode"] == "kick":
            await message.chat.ban_member(user_id, until_date=int(time() + 45))
            action = "kicked"
        elif warn_settings["warn_mode"] == "ban":
            await message.chat.ban_member(user_id)
            action = "banned"
        elif warn_settings["warn_mode"] == "mute":
            await message.chat.restrict_member(user_id, ChatPermissions())
            action = "muted"
        return await message.reply_text(
            (
                f"Warnings {num}/{warn_settings['warn_limit']}!"
                f"\n<b>Reason for last warn</b>:\n{reason}"
                if reason
                else "\n"
                f"{(await mention_html(user_first_name, user_id))} has been <b>{action}!</b>"
            ),
            reply_to_message_id=r_id,
        reply_markup=keyboard    
        )
    if message.text.split()[0] == "/swarn":
        await message.delete()
        await message.stop_propagation()
    if message.text.split()[0] == "/dwarn":
        if not message.reply_to_message:
            await message.reply_text(_["warn3"])
            await message.stop_propagation()
        await message.reply_to_message.delete()
    txt = f"""
**be careful** {(await mention_html(user_first_name, user_id))} ❗️

**Warned By:** {message.from_user.mention if message.from_user else 'none'}
**Reason:** {reason or 'No Reason Provided.'}
**Warns:** {num}/{warn_settings['warn_limit']}

    """
    await message.reply_text(
        txt,
        reply_to_message_id=r_id,
        reply_markup=keyboard
    )
    await message.stop_propagation()



@app.on_message(command("resetwarns") & restrict_filter )
@language
async def reset_warn(client, message: Message, _):  
    user_id, user_first_name, _ = await extract_user(app, message)
    warn_db = Warns(message.chat.id)
    warn_db.reset_warns(user_id)
    await message.reply_text(_["warn5"].format((await mention_html(user_first_name, user_id))))
    return

@app.on_message(filters.command("resetallwarns") & restrict_filter)
@language
async def clear_warns(client, message: Message, _):     
    warn_db = WarnSettings(message.chat.id)
    warns = warn_db.getall_warns()
    if not warns:
        await message.reply_text(_["warn6"])
        return

    await message.reply_text(_["warn6"],
        reply_markup=ikb(
            [[("♻️ Reset all warnings ", "clear_warns"), ("✖️ Close ", "close_data")]],
        ),
    )
    return



@app.on_message(command("warns"))
@language
async def list_warns(client, message: Message, _): 
    user_id, user_first_name, _ = await extract_user(app, message)
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(message, "warns"))}

    if user_id in admins_group:
        await message.reply_text(_["warn8"],
        )
        return

    warn_db = Warns(message.chat.id)
    warn_settings_db = WarnSettings(message.chat.id)
    warns, num_warns = warn_db.get_warns(user_id)
    warn_settings = warn_settings_db.get_warnings_settings()
    if not warns:
        await message.reply_text(_["warn9"])
        return
    msg = f"{(await mention_html(user_first_name,user_id))} has <b>{num_warns}/{warn_settings['warn_limit']}</b> warns!\n\n<b>Reasons:</b>\n"
    msg += "\n".join([("- No reason" if i is None else f" - {i}") for i in warns])
    await message.reply_text(msg)
    return


@app.on_message(command(["rmwarn", "removewarn"]) & restrict_filter)
@language
async def remove_warn(client, message: Message, _):
    if not len(message.command) > 1 and not message.reply_to_message:
        await message.reply_text(_["warn10"])
        return

    user_id, user_first_name, _ = await extract_user(app, message)

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(message, "rmwarn"))}

    if user_id in admins_group:
        await message.reply_text(_["warn11"])
        return

    warn_db = Warns(message.chat.id)
    warns, _ = warn_db.get_warns(user_id)
    if not warns:
        await message.reply_text(_["warn12"])
        return

    _, num_warns = warn_db.remove_warn(user_id)
    await message.reply_text(
        (
            f"{(await mention_html(user_first_name,user_id))} now has <b>{num_warns}</b> warnings!\n"
            "Their last warn was removed."
        ),
    )
    return await message.chat.unban_member(user_id)




@app.on_message(command(["warnings", "warnsettings"]) & admin_filter)
@language
async def get_settings(client, message: Message, _):
    warn_settings_db = WarnSettings(message.chat.id)
    settings = warn_settings_db.get_warnings_settings()
    await message.reply_text(
        (
            "This group has these following settings:\n"
            f"<b>Warn Limit:</b> <code>{settings['warn_limit']}</code>\n"
            f"<b>Warn Mode:</b> <code>{settings['warn_mode']}</code>"
        ),
    )
    return


@app.on_message(command("warnmode") & admin_filter)
@language
async def warnmode(client, message: Message, _):  
    warn_settings_db = WarnSettings(message.chat.id)
    if len(message.text.split()) > 1:
        wm = (message.text.split(None, 1)[1]).lower()
        if wm not in ("kick", "ban", "mute"):
            await message.reply_text(_["warn15"])
            return
        warnmode_var = warn_settings_db.set_warnmode(wm)
        await message.reply_text(_["warn13"].format(warnmode_var))
        return
    warnmode_var = warn_settings_db.get_warnmode()
    await message.reply_text(_["warn14"].format(warnmode_var))
    return


@app.on_message(command("warnlimit") & admin_filter)
@language
async def warnlimit(client, message: Message, _):
    warn_settings_db = WarnSettings(message.chat.id)
    if len(message.text.split()) > 1:
        wl = int(message.text.split(None, 1)[1])
        if not isinstance(wl, int):
            await message.reply_text(_["warn16"])
            return
        warnlimit_var = warn_settings_db.set_warnlimit(wl)
        await message.reply_text(_["warn17"].format(warnlimit_var))
        return
    warnlimit_var = warn_settings_db.get_warnlimit()
    await message.reply_text(_["warn18"].format(warnlimit_var))
    return

__MODULE__ = Warnin
__HELP__ = """
Keep your members in check with warnings; stop them getting out of control!
If you're looking for automated warnings, go read about the blocklist module.

**Admin commands:**
- /warn `<reason>`: Warn a user.
- /dwarn `<reason>`: Warn a user by reply, and delete their message.
- /swarn `<reason>`: Silently warn a user, and delete your message.
- /warns: See a user's warnings.
- /rmwarn: Remove a user's latest warning.
- /resetwarn: Reset all of a user's warnings to 0.
- /resetallwarns: Delete all the warnings in a chat. All users return to 0 warns.
- /warnings: Get the chat's warning settings.
- /warnmode `<ban/kick/mute/tban/tmute>`: View or set the chat's warn mode.
- /warnlimit `<number>`: View or set the number of warnings before users are punished.

**Examples:**
- Warn a user.
- `/warn @user For disobeying the rules`
"""
