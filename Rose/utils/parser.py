from html import escape
from re import compile as compilere
from re import sub
from pyrogram.types import InlineKeyboardButton

async def cleanhtml(raw_html: str) -> str:
    cleanr = compilere("<.*?>")
    return sub(cleanr, "", raw_html)


async def escape_markdown(text: str) -> str:
    escape_chars = r"\*_`\["
    return sub(r"([%s])" % escape_chars, r"\\\1", text)


async def mention_html(name: str, user_id: int) -> str:
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def mention_markdown(name: str, user_id: int) -> str:
    return f"[{(await escape_markdown(name))}](tg://user?id={user_id})"


def parser(text):
    btn_regex = compile(r"(\[([^\[]+?)\]\((link|cdata):(?:/{0,2})(.+?)(:same)?\))")
    if "alert" in text:
        text = (text.replace("\n", "\\n").replace("\t", "\\t"))
    buttons, outtext, prev = [],"", 0
    for match in btn_regex.finditer(text):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        if n_escapes % 2 == 0:
            outtext += text[prev:match.start(1)]
            prev = match.end(1)
            if match.group(3) == "cdata":
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=match.group(4).replace(" ", "")))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=match.group(4).replace(" ", ""))])
            elif bool(match.group(5)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", "")))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", ""))])
        else:
            outtext += text[prev:to_check]
            prev = match.start(1) - 1
    outtext += text[prev:]
    try:
        return outtext, buttons
    except:
        return outtext, buttons