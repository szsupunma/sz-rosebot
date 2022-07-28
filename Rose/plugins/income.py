import asyncio
import requests
from os import remove
from pyrogram import filters
from pyrogram.types import Message
from Rose.utils.filter_groups import spam,spoiler,channel,url,porn
from typing import Union
from Rose.plugins.protection import get_file_id
from Rose.mongo.approvedb import Approve 
from Rose import app as pbot,app
from Rose.core.decorators.permissions import list_admins,member_permissions
from Rose.plugins.lock import lockdb

del_message = "{}, Your message was deleted as it contain a {}. \n ❗️ {} are not allowed here"


@pbot.on_message(filters.audio  & ~filters.private  & ~filters.linked_channel  & ~filters.bot)
async def audiolock(client, message):
    if lockdb.find_one({"aud": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Audio","Audio"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()


@pbot.on_message(filters.video & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def videolock(client, message):
    if lockdb.find_one({"vid": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return    
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Video","Video"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()


@pbot.on_message(filters.document & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def doclock(client, message):
    if not message.chat:
      return    
    if lockdb.find_one({"doc": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Document","Document"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()
        
@pbot.on_message(filters.text & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def emaeil(client, message):
    if not message.chat:
        message.continue_propagation()
    if lockdb.find_one({"email": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    texct = message.text
    if "@gmail.com" in texct:
        try:
            supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Email","Email"))
            await asyncio.sleep(5)
            await supun.delete()
            await message.delete()
        except:
            message.continue_propagation()      
    if "@outlook.com" in texct:
        try:
            supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Email","Email"))
            await asyncio.sleep(5)
            await supun.delete()
            await message.delete()
        except:
            message.continue_propagation()  
    if "@hotmail.com" in texct:
        try:
            supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Email","Email"))
            await asyncio.sleep(5)
            await supun.delete()
            await message.delete()
        except:
            message.continue_propagation()  
    if "@edumail.com" in texct:
        try:
            supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Email","Email"))
            await asyncio.sleep(5)
            await supun.delete()
            await message.delete()
        except:
            message.continue_propagation()
    if "mail.com" in texct:
        try:
            supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Email","Email"))
            await asyncio.sleep(5)
            await supun.delete()
            await message.delete()
        except:
            message.continue_propagation()
    message.continue_propagation()
    
@pbot.on_message(filters.forwarded & ~filters.private  & ~filters.linked_channel & ~filters.bot)
async def fwd(client, message):
    if not message.chat:
      return    
    if lockdb.find_one({"fwd": message.chat.id}):
        pass
    else:
        message.continue_propagation() 
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return   
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Forward","Forward"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()

@pbot.on_message(filters.sticker & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def slock(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"stc": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"sticker","Sticker"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()

@pbot.on_message(filters.animation & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def aalock(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"gif": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return    
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Gif","Gif"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()

@pbot.on_message(filters.game & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def aggalock(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"game": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return      
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Game","Game"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()

@pbot.on_message(filters.incoming & filters.media_group & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggsjalock(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"albm": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Game","Game"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except Exception as e:
        print(e)
        message.continue_propagation()       
         
@pbot.on_message(filters.voice & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggalgossck(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"voice": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return      
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Voice","Voice"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()     
        
@pbot.on_message(filters.video_note & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggalock(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"vnote": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return    
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Video_note","Video_note"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()                                 
             
@pbot.on_message(filters.contact & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"contact": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Contact","Contact"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()             
        
@pbot.on_message(filters.location & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"gps": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Location","Location"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation() 
        
@pbot.on_message(filters.venue & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"address": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Venue","Venue"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()     
                                                                     
@pbot.on_message(filters.reply & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def reply(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"reply": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return   
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Reply","Reply"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()                                                                                                                                    
              
@pbot.on_message(filters.text & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def messages(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"message": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return    
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Message","Message"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()        
    
@pbot.on_message(filters.edited & ~filters.private  & ~filters.linked_channel & ~filters.bot)
async def edt(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"edit": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return     
    try:
        try:
         await message.delete()
         supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Edited","Edited"))
         await asyncio.sleep(5)
         await supun.delete() 
        except:
             message.continue_propagation()
    except:
        message.continue_propagation()     

@pbot.on_message(filters.incoming  & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def mnsn(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"mention": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    textl = message.text
    textl = str(textl)
    if "@" not in textl:
        return message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return 
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Mention","Mention"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()    
      

@pbot.on_message(filters.via_bot & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def inln(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"inline": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    try:
        supun = await app.send_message(chat_id = message.chat.id, text = del_message.format(message.from_user.mention,"Inline","Inline"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()       

@pbot.on_message(filters.poll & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def poll(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"poll": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Poll","Poll"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()               

@pbot.on_message(filters.incoming & filters.dice & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def diced(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"dice": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Dice","Dice"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()             


@pbot.on_message(filters.inline_keyboard & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def button(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"button": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return 
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Inline_keyboard","Inline_keyboard"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()
             
@pbot.on_message(filters.photo & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def mediwa(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"pic": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return   
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Photo","Photo"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()     

@pbot.on_message(filters.media & ~filters.private & ~filters.linked_channel & ~filters.bot)
async def mediwa(client, message):
    if not message.chat:
      return
    if lockdb.find_one({"media": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_users = Approve(message.chat.id).list_approved()
    chats = [user[0] for user in approved_users]
    for c in chats:
        if message.from_user.id == int(c):
            return   
    try:
        supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Media","Media"))
        await asyncio.sleep(5)
        await supun.delete()
        await message.delete()
    except:
        message.continue_propagation()

 
@app.on_message(
        filters.incoming 
        | ~filters.linked_channel,
        group=url
)
async def urls(client, message):  
    if not message.chat:
        return    
    lel = get_url(message)
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if lel:
        if not lockdb.find_one({"url": message.chat.id}):
           return
        if user_id in await list_admins(message.chat.id):
            return  
        try:
         await message.delete()
         supun = await app.send_message(chat_id = message.chat.id,text = del_message.format(message.from_user.mention,"Url","Url"))
         await asyncio.sleep(5)
         await supun.delete()
        except:
             message.continue_propagation()
    else:
            message.continue_propagation()

@app.on_message(
        filters.incoming 
        | ~filters.linked_channel,
        group=porn
)
async def porn_hub(client, message):  
    if not message.chat:
        return
    file_id = get_file_id(message)
    if not file_id:
        return
    file = await app.download_media(file_id)
    try:
        data = requests.post("https://api.safone.tech/nsfw", files={'image': open(file, 'rb')}).json()

        is_nsfw = data['data']['is_nsfw']
        neutral = data['data']['neutral']
        hentai = data['data']['hentai']
        drawings = data['data']['drawings']
        porn = data['data']['porn']
        sexy = data['data']['sexy']
    except Exception:
        return
    remove(file)
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if is_nsfw == "true":
        if not lockdb.find_one({"porn": message.chat.id}):
           return
        if user_id in await list_admins(message.chat.id):
            return  
        try:
         await message.delete()
         sender = message.from_user.mention()
         lol = await pbot.send_message(message.chat.id,f"""
{sender}, Your message was deleted as it contain porn(s). 

==========================
• **Porn:** `{porn} %`
• **Neutral:** `{neutral} %`
• **Hentai:** `{hentai} %`
• **Sexy:** `{sexy} %`
• **Drawings:** `{drawings} %`
• **NSFW:** `{is_nsfw}`
==========================

❗️ porns are not allowed here""")
         await asyncio.sleep(7)
         await lol.delete()   
        except:
             message.continue_propagation()
    else:
            message.continue_propagation()

@app.on_message(filters.incoming  & ~filters.linked_channel, group=channel)
async def channel(client, message):
    chat_id = message.chat.id
    if message.sender_chat:
        sender = message.sender_chat
        if message.forward_from_chat and not message.from_user : return
        if not lockdb.find_one({"anonchannel": message.chat.id}) or lockdb.find_one({"channel": message.chat.id}):
            return 
        if chat_id == sender.id:
            return
        await message.delete()
        ti = await message.reply_text(f"{sender.title}, Your message was deleted as it from channel(s). \n ❗️ channel are not allowed here")
        await asyncio.sleep(10)
        await ti.delete()

@app.on_message(
        ~filters.private
        | ~filters.linked_channel
        | filters.text,
        group=spoiler
)
async def spoiler(client, message):
    if not message.chat:
      return  
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if not lockdb.find_one({"spoiler": message.chat.id}):
        return
    if message.entities:     
     for entity in message.entities:
        if entity.type == "spoiler":
            try:
               await message.delete()  
               sender = message.from_user.mention()
               lol = await pbot.send_message(message.chat.id,f"{sender}, Your message was deleted as it contain a spoiler(s). \n ❗️ spoilers are not allowed here")
               await asyncio.sleep(10)
               await lol.delete()   
            except:
              message.continue_propagation() 

def get_url(message_1: Message) -> Union[str, None]:
    messages = [message_1]
    if message_1.reply_to_message:
        messages.append(message_1.reply_to_message)
    text = ""
    offset = None
    length = None
    for message in messages:
        if offset:
            break
        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break
    if offset in (None,):
        return None
    return text[offset : offset + length]

@app.on_message(
        filters.incoming 
        | ~filters.linked_channel,
        group=spam
)
async def spam_locked(client, message):  
    if not message.chat:
        return
    try:
        data = requests.post("https://api.safone.tech/spam", json={'text': message.text}).json()

        is_spam = data['data']['is_spam']
        spam_probability = data['data']['spam_probability']
        spam = data['data']['spam']
        ham = data['data']['ham']
    except Exception:
        return
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if is_spam=="true":

        if not lockdb.find_one({"spam": message.chat.id}):
           return
        if user_id in await list_admins(message.chat.id):
            return  
        try:
         await message.delete()
         sender = message.from_user.mention()
         lol = await pbot.send_message(message.chat.id,f"""
{sender}, Your message was deleted as it contain spam(s). 

==========================
• **Is Spam:** `{is_spam}`
• **Spam Probability:** `{spam_probability}` %
• **Spam:** `{spam}`
• **Ham:** `{ham}`
==========================

❗️ spam are not allowed here""")
         await asyncio.sleep(7)
         await lol.delete()   
        except:
             message.continue_propagation()
    else:
            message.continue_propagation()