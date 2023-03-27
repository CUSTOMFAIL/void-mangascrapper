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
    if event.sender_id == 1902388715 or event.sender_id == 1719179612:
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
                            icon_path = r.download_icon("./icon.png")
                            chapters = r.chapter_list
                            for c in chapters:
                                app = (f"#{c.chapter} | {c.title}")
                                chap.append(app)
                            print(r.title, r.views)
                            await client.send_file(event.chat_id, file = icon_path, caption = "Chapter found :{}".format(len(chap)))
                            os.remove(icon_path)
                            chapters = r.chapter_list
                            print("done")
                            for c in chapters:
                                print("started")
                                print(f"#{c.chapter} | {c.title}")
                                print("Chapter {} - {}.pdf".format(z, lis[int(a)]))
                                chapter_path = c.download(r"./Chapter {} - {}.pdf".format(c.chapter, lis[int(a)]))
                                await client.send_file(event.chat_id, file = chapter_path, caption = "@manhwa_uploads", thumb = r"thumb.jpg")
                                os.remove(chapter_path)
                                z +=1
                            await client.send_message(event.chat_id, "COMPLETED")







client.start()
client.run_until_disconnected()
