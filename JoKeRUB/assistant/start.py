#    جميع الحقوق لمطوري سورس جـيبثون حصريا لهم فقط
#    اذا تخمط الملف اذك الحقوق وكاتبيه ومطوريه لا تحذف الحقوق وتصير فاشل 👍
#    كتابة الشسد 
import asyncio
import io
import re
import os
from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest
from JoKeRUB import bot
from JoKeRUB.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from JoKeRUB.sql_helper.botusers_sql import add_me_in_db, his_userid
from JoKeRUB.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)
from l313l.razan.resources.assistant import *
from sai import gpt  # استيراد وظيفة gpt

# إنشاء بوت Telegram
TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

bot = telebot.TeleBot(TOKEN)

# بدء وظيفة gptMessage
@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.text.startswith('/p '):
        question = message.text[3:]  # استخرج السؤال بعد الأمر /p
        resp = gpt(question)  # أزل معالجة الأخطاء
        bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')

#start 
@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    rehu = await tgbot.get_me()
    bot_id = rehu.first_name
    bot_username = rehu.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.users[0].first_name
    vent = event.chat_id
    starttext = f"**مـرحبا {firstname} ! انـا هـو {bot_id}, بـوت مساعـد بسيـط  \n\n- [مـالك البـوت](tg://user?id={bot.uid}) \nيمكـنك مراسلـة المـالك عبـر هذا البـوت . \n\nاذا كـنت تـريد تنـصيب بـوت خـاص بـك تـاكد من الازرار بالأسفل**"
    
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"**اهـلا يا مالكـي انـه انـا {bot_id}, مسـاعدك  \nمـاذا تريـد ان تفعـل اليـوم **",
            buttons=[
                [Button.inline("عرض المستخدمين ", data="users"), Button.inline("اوامر البـوت ", data="gibcmd")],
                [Button.url("المطـور محمد", "https://t.me/Zo_r0")],
                [Button.url("المطـور علوش", "https://t.me/I_e_e_l")],
            ]
        )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_message(
            event.chat_id,
            message=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("تنـصيب العقرب 🦂", data="deploy")],
                [Button.url("تحتاج مسـاعدة ", "https://t.me/Zo_r0")],
            ],
        )

# Data
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
            message="**لتـنصيب البـوت الخاص بك اتبـع الخطـوات في الاسفـل وحاول واذا لم تستطيع تفضل الى مجموعة المساعدة ليساعدوك 🧸♥**.",
            buttons=[
                [Button.url("كروب المساعدة ", "https://t.me/Scorpions_scorp")],
            ],
        )

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "- قـائمة مستخـدمين البـوت  : \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "Scorpion.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                caption="مجموع مستخدمـين بوتـك",
                allow_cache=False,
            )
    else:
        pass

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
    await event.delete()
    rorza = "** قـائمـة اوامـر بوت العقرب الخاصـة بك **:\n\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات\n\n• /start \n ( للـتأكد من حالـة البـوت) \n\n• /ping \n ( امـر بنـك )  \n\n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n\n• /id \n  ( لعـرض ايدي المسـتخدم ) \n\n• /alive \n- ( لـرؤية معلومات البـوت ) \n\n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n\n• /prumote  \n-  ( لرفـع شخص مشـرف )\n\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n\n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n\n• /stats  \n-  ( لعرض مستخدمين البوت )  \n\n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n\n• /del  \n-  ( بالـرد على الرسالـة لحـذفها ) \n\n [العقرب | 𝗦𝗰𝗼𝗿𝗽𝗶𝗼 🦂](t.me/Scorpions_scorp)**"
    await tgbot.send_message(event.chat_id, rorza)

@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    rorza = "** قـائمـة اوامـر بوت العقرب الخاصـة بك **:\n\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات\n\n• /start \n ( للـتأكد من حالـة البـوت) \n\n• /ping \n ( امـر بنـك )  \n\n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n\n• /id \n  ( لعـرض ايدي المسـتخدم ) \n\n• /alive \n- ( لـرؤية معلومات البـوت ) \n\n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n\n• /prumote  \n-  ( لرفـع شخص مشـرف )\n\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n\n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n\n• /stats  \n-  ( لعرض مستخدمين البوت )  \n\n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n\n• /del  \n-  ( بالـرد على الرسالـة لحـذفها ) \n\n [العقرب | 𝗦𝗰𝗼𝗿𝗽𝗶𝗼 🦂](t.me/Scorpions_scorp)**"
    await event.reply(rorza)

@tgbot.on(events.NewMessage(pattern="^/alive", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    razan = "**بوت العقرب**\n\n**- حالة البوت **  يعمـل بنجـاح\n**- اصدار التليثون  **: 1.23.0\n**- اصدار البايثون **: 3.10.9\n\n**العقرب |  𝗦𝗰𝗼𝗿𝗽𝗶𝗼 🦂**\n"
    await event.reply(razan)

# بدء تشغيل البوت
if __name__ == "__main__":
    bot.polling(none_stop=True)
