from datetime import datetime, timedelta
from os import execvp
from re import findall
from re import sub as re_sub
from sys import executable
from pyrogram.types import Message
from Rose import aiohttpsession as aiosession
from Rose.mongo.restart import *


async def restart(m: Message):
    if m:
        await start_restart_stage(m.chat.id, m.message_id)
    execvp(executable, [executable, "-m", "Rose"])

async def get_http_status_code(url: str) -> int:
    async with aiosession.head(url) as resp:
        return resp.status

def get_urls_from_text(text: str) -> bool:
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]
                [.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(
                \([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
                ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
    return [x[0] for x in findall(regex, str(text))]


async def time_converter(message: Message, time_value: str) -> int:
    unit = ["m", "h", "d"]  # m == minutes | h == hours | d == days
    check_unit = "".join(list(filter(time_value[-1].lower().endswith, unit)))
    currunt_time = datetime.now()
    time_digit = time_value[:-1]
    if not time_digit.isdigit():
        return await message.reply_text("Incorrect time specified")
    if check_unit == "m":
        temp_time = currunt_time + timedelta(minutes=int(time_digit))
    elif check_unit == "h":
        temp_time = currunt_time + timedelta(hours=int(time_digit))
    elif check_unit == "d":
        temp_time = currunt_time + timedelta(days=int(time_digit))
    else:
        return await message.reply_text("Incorrect time specified.")
    return int(datetime.timestamp(temp_time))


async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True
    text = text.strip()
    if is_int(text):
        return int(text)
    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.from_user:
            id_ = reply.from_user.id

        elif (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
            id_ = reply.sender_chat.id
        else:
            return None, None
        reason = None if len(args) < 2 else text.split(None, 1)[1]
        return id_, reason
    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None
    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


def get_file_id_from_message(
    message,
    max_file_size=3145728,
    mime_types=["image/png", "image/jpeg"],
):
    file_id = None
    if message.document:
        if int(message.document.file_size) > max_file_size:
            return

        mime_type = message.document.mime_type

        if mime_types and mime_type not in mime_types:
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


def extract_text_and_keyb(ikb, text: str, row_width: int = 2):
    keyboard = {}
    try:
        text = text.strip()
        text = text.removeprefix("`")
        text = text.removesuffix("`")
        text, keyb = text.split("~")

        keyb = findall(r"\[.+\,.+\]", keyb)
        for btn_str in keyb:
            btn_str = re_sub(r"[\[\]]", "", btn_str)
            btn_str = btn_str.split(",")
            btn_txt, btn_url = btn_str[0], btn_str[1].strip()

            if not get_urls_from_text(btn_url):
                continue
            keyboard[btn_txt] = btn_url
        keyboard = ikb(keyboard, row_width)
    except Exception:
        return
    return text, keyboard


async def get_user_id_and_usernames(client) -> dict:
    with client.storage.lock, client.storage.conn:
        users = client.storage.conn.execute(
            'SELECT * FROM peers WHERE type in ("user", "bot") AND username NOT null'
        ).fetchall()
    users_ = {}
    for user in users:
        users_[user[0]] = user[3]
    return users_
