from telethon.tl.types import MessageEntityCode
from telethon import TelegramClient, events, Button
import telethon.sync
import os
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon import functions
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.types import InputPeerChannel
import pymongo
import random
import requests
import string
from pymongo import MongoClient
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    UserBlockedError,
    ChatWriteForbiddenError,
)
import manganelo


api_id = 12821547
api_hash = '8205f50ad9bec97db4040196a0ccc853'
bot_token = os.environ.get("TOKEN")




client = TelegramClient('hakudjwsa', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage)
async def create(event):
    lis = [1943966786, 5437374877, 5531584953, 1925191075, 1978265149, 1719179612]
    if event.sender_id in lis:
        if event.text == "/start":
            await event.reply("Send any manga, manhwa or manhua name")
        else:
            home_page = manganelo.get_home_page()
            results = manganelo.get_search_results(str(event.text))
            text = ""
            num = 1
            z = 1
            lis = [""]
            for r in results:
                text += "{}. {}\n".format(str(num), r.title)
                num +=1
                lis.append(r.title)
            chap = []
            if text == "":
                await event.reply("Not found")
            else:
                print(lis)
                async with client.conversation(event.sender_id) as conv:
                    res = await conv.send_message("Enter the number : \n\n`{}`".format(str(text)))
                    naruto = await conv.get_response(timeout = 90000)
                    a = naruto.text
                    alpha = ""
                    try:
                        beta = a.split(" ")
                        beta = alpha.join(beta)
                    except Exception as e:
                        beta = a
                    print("Beta =  {}".format(beta))
                    delta = a.isnumeric()
                    eta = beta.isalpha()
                    while eta == True and delta == False:
                        print("a was alpha")
                        home_page = manganelo.get_home_page()
                        results = manganelo.get_search_results(str(a))
                        text = ""
                        num = 1
                        z = 1
                        lis = [""]
                        lu = [""]
                        for r in results:
                            text += "{}. {}\n".format(str(num), r.title)
                            num +=1
                            lis.append(r.title)
                        chap = []
                        print("reached")
                        print(text)
                        if text == "":
                            await event.reply("Not found")
                        else:
                            print(lis)
                            await conv.send_message("Enter the number : \n\n`{}`".format(str(text)))
                            sas = await conv.get_response(timeout = 90000)
                            print("sent")
                            a = sas.text
                            alpha = ""
                            try:
                                beta = a.split(" ")
                                beta = alpha.join(beta)
                            except Exception as e:
                                beta = a
                            print("Beta =  {}".format(beta))
                            delta = a.isnumeric()
                            eta = beta.isalpha()
                    print(lis[int(a)])
                    results = manganelo.get_search_results(event.text)
                    for r in results:
                        if r.title == lis[int(a)]:
                            chapters = r.chapter_list
                            for c in chapters:
                                app = (f"#{c.chapter} | {c.title}")
                                chap.append(app)
                            print(r.title, r.views)
                            mg = "1. DOWNLOAD ALL\n2. ENTER FROM WHERE TO WHERE\n3. ENTER A CHAPTER NO.\n4. DOWNLOAD LAST CHAPTER"
                            await conv.send_message("Enter the number : \n\n`{}`".format(str(mg)))
                            mgres = await conv.get_response(timeout = 90000)
                            error = ""
                            chaperror = ""
                            message = await client.send_message(event.chat_id, "Name : {}\n\nChapter found :{}\n\nSTARTING DOWNLOAD".format(r.title, len(chap)))
                            await client.pin_message(event.chat_id, message, notify=True)
                            chapters = r.chapter_list
                            print("done")
                            if mgres.text == 1 or mgres.text == "1":
                                for c in chapters:
                                    print("started")
                                    print(f"#{c.chapter} | {c.title}")
                                    print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                    try:
                                        chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                        await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_region", thumb = r"thumb.png")
                                        os.remove(chapter_path)
                                        z +=1
                                    except Exception as e:
                                        error = "COULD NOT DOWNLOAD CHAPTER NO. {}. PLEASE DOWNLOAD IT MANUALLY".format(c.chapter)
                                        await client.send_message(event.chat_id, error)
                                        chaperror += "{}\n".format(c.chapter)
                            elif mgres.text == 2 or mgres.text == "2":
                                await conv.send_message("Enter from which chapter you have to download:\n(For example if you have to download from 15 to 65. Enter 15\n\nJust a friendly suggestion if you want to download from 15 to 65 use 14 instead so that u wont miss any sub chapter like 14.9 or 15.0)")
                                minint = await conv.get_response(timeout = 90000)
                                minint = minint.text
                                minint = int(minint)
                                await conv.send_message("Enter till which chapter you have to download:\n(For example if you have to download from 15 to 65. Enter 65\n\nIf you want to download till last chapter enter: -1\n\nJust a friendly suggestion if you want to download from 15 to 65 use 66 instead so that u wont miss any sub chapter like 65.1 or 65.2)")
                                maxint = await conv.get_response(timeout = 90000)
                                maxint = maxint.text
                                maxint = int(maxint)
                                for c in chapters:
                                    if maxint == -1:
                                        if int(c.chapter) >= minint:
                                            print("started")
                                            print(f"#{c.chapter} | {c.title}")
                                            print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                            try:
                                                chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                                await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_region", thumb = r"thumb.png")
                                                os.remove(chapter_path)
                                                z +=1
                                            except Exception as e:
                                                error = "COULD NOT DOWNLOAD CHAPTER NO. {}. PLEASE DOWNLOAD IT MANUALLY".format(c.chapter)
                                                await client.send_message(event.chat_id, error)
                                                chaperror += "{}\n".format(c.chapter)
                                    else:      
                                        if int(c.chapter) >= minint and int(c.chapter) <= maxint:
                                            print("started")
                                            print(f"#{c.chapter} | {c.title}")
                                            print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                            try:
                                                chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                                await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_region", thumb = r"thumb.png")
                                                os.remove(chapter_path)
                                                z +=1
                                            except Exception as e:
                                                error = "COULD NOT DOWNLOAD CHAPTER NO. {}. PLEASE DOWNLOAD IT MANUALLY".format(c.chapter)
                                                await client.send_message(event.chat_id, error)
                                                chaperror += "{}\n".format(c.chapter)
                                            
                            elif mgres.text == 3 or mgres.text == "3":
                                await conv.send_message("Enter from which chapter you have to download:\n(For example if you have to download from 15 to 65. Enter 15)")
                                chapnum = await conv.get_response(timeout = 90000)
                                chapnum = int(chapnum.text)
                                for c in chapters:
                                    if int(c.chapter) == chapnum:
                                        print("started")
                                        print(f"#{c.chapter} | {c.title}")
                                        print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                        try:
                                            chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                            await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_region", thumb = r"thumb.png")
                                            os.remove(chapter_path)
                                            z +=1
                                        except Exception as e:
                                            error = "COULD NOT DOWNLOAD CHAPTER NO. {}. PLEASE DOWNLOAD IT MANUALLY".format(c.chapter)
                                            await client.send_message(event.chat_id, error)
                                            chaperror += "{}\n".format(c.chapter)
                            elif mgres.text == 4 or mgres.text == "4":
                                lst = []
                                for c in chapters:
                                    lst.append(int(c.chapter))
                                for c in chapters:
                                    if int(c.chapter) == int(lst[-1]):
                                        print("started")
                                        print(f"#{c.chapter} | {c.title}")
                                        print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                        try:
                                            chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                            await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_region", thumb = r"thumb.png")
                                            os.remove(chapter_path)
                                            z +=1
                                        except Exception as e:
                                            error = "COULD NOT DOWNLOAD CHAPTER NO. {}. PLEASE DOWNLOAD IT MANUALLY".format(c.chapter)
                                            await client.send_message(event.chat_id, error)
                                            chaperror += "{}\n".format(c.chapter)
                                
                            else:
                                pass
                            if chaperror != "":
                                await client.send_message(event.chat_id, "COMPLETED\n\nPlease dowmload these chapter manually\n{}".format(chaperror))
                            else:
                                await client.send_message(event.chat_id, "  COMPLETED")
                            print("completed")







client.start()
client.run_until_disconnected()
