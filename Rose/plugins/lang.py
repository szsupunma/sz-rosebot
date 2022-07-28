from lang import get_string
from Rose.mongo.language import set_lang,get_lang
from Rose import app,LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,Message
from Rose.utils.lang import language
from button import Languages


keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="🇱🇷 English", callback_data="languages_en")],
     [InlineKeyboardButton(text="🇱🇰 සිංහල", callback_data="languages_si"), 
      InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="languages_hi")], 
     [InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="languages_it"), 
      InlineKeyboardButton(text="🇮🇳 తెలుగు", callback_data="languages_ta")], 
     [InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data="languages_id"), 
      InlineKeyboardButton(text="🇦🇪 عربي", callback_data="languages_ar")], 
     [InlineKeyboardButton(text="🇮🇳 മലയാളം", callback_data="languages_ml"), 
      InlineKeyboardButton(text="🇲🇼 Chichewa", callback_data="languages_ny")], 
     [InlineKeyboardButton(text="🇩🇪 German", callback_data="languages_ge"), 
      InlineKeyboardButton(text="🇷🇺 Russian", callback_data="languages_ru")]])


@app.on_message(filters.command("lang"))
@language
async def langs_command(client, message: Message, _):
    userid = message.from_user.id if message.from_user else None
    chat_type = message.chat.type
    if chat_type == "private":await message.reply_text("Choose Your languages",reply_markup=keyboard)
    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id
        st = await app.get_chat_member(group_id, userid)
        if st.status not in ["administrator", "creator"]:
            return
        try:   
         await message.reply_text( "Choose Your languages",reply_markup=keyboard)
        except Exception as e:
         return await app.send_message(LOG_GROUP_ID,text= e)


@app.on_callback_query(filters.regex("languages"))
async def language_markup(_, CallbackQuery):
    langauge = (CallbackQuery.data).split("_")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
      return await CallbackQuery.answer("⛔️ You're already on same language")
    await set_lang(CallbackQuery.message.chat.id, langauge)
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer("✅ Successfully changed your language.")
    except:
        return await CallbackQuery.answer(
            "This language is Under Construction 👷")
    await set_lang(CallbackQuery.message.chat.id, langauge)
    return await CallbackQuery.message.edit(f"{CallbackQuery.message.from_user.mention} Was Successfully changed My language ✅\n From {old} to {langauge}")

__MODULE__ = f"{Languages}"
__HELP__ = """
Not every group speaks fluent english; some groups would rather have Rose respond in their own language.

This is where translations come in; you can change the language of most replies to be in the language of your choice!

**Admin commands:**
- /lang : Set your preferred language.
"""
__helpbtns__ = (
    [[InlineKeyboardButton(text="🇱🇷 English", callback_data="languages_en")],
     [InlineKeyboardButton(text="🇱🇰 සිංහල", callback_data="languages_si"), 
      InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="languages_hi")], 
     [InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="languages_it"), 
      InlineKeyboardButton(text="🇮🇳 తెలుగు", callback_data="languages_ta")], 
     [InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data="languages_id"), 
      InlineKeyboardButton(text="🇦🇪 عربي", callback_data="languages_ar")], 
     [InlineKeyboardButton(text="🇮🇳 മലയാളം", callback_data="languages_ml"), 
      InlineKeyboardButton(text="🇲🇼 Chichewa", callback_data="languages_ny")], 
     [InlineKeyboardButton(text="🇩🇪 German", callback_data="languages_ge"), 
      InlineKeyboardButton(text="🇷🇺 Russian", callback_data="languages_ru")]])
