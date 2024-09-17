# bot_handler.py

import asyncio
from telethon import events
from telethon.errors import YouBlockedUserError
from gpt import gpt  # استيراد دالة gpt من الملف الأول

from JoKeRUB import l313l
from . import l313l
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "البوت"

@l313l.ar_cmd(pattern="سو(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()

    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**✎┊‌ بالرد على السؤال او بأضافة سؤال \n يعني تكتب (`.سؤال`) وبعده سؤالك وخلص 😌 \n\n مثال : \n `.سؤال من هو مخترع الكهرباء`**")
    if not question and event.reply_to_msg_id and reply_message.text: 
        question = reply_message.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)

    response_msg = await edit_or_reply(event, "**✎┊‌اصبر حبيبي هسة يجاوبك 😁**")

    try:
        # استخدام دالة `gpt` من ملف gpt_module.py
        answer = gpt(question)
        if "understanding" in answer:
            answer = "**- عـذرًا .. لم أفهم سؤالك\n- قم بـ إعادة صياغته من فضلك؟!**"
        await response_msg.delete()
        await event.client.send_message(event.chat_id, f"**السؤال : {question}\n\n{answer}**\n\n───────────────────\n")
    except Exception as e:
        await response_msg.edit(f"**حدث خطأ: {str(e)}**")
