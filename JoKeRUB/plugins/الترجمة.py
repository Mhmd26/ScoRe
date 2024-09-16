from asyncio import sleep
import requests
import json
import os
from JoKeRUB.helpers.functions.functions import translate
from JoKeRUB import l313l
from telethon import events, types
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import soft_deEmojify

langs = {
    'عربي': 'ar',
    'فارسي': 'fa',
    'بلغاري': 'bg',
    'صيني مبسط': 'zh',
    'صيني تقليدي': 'zh-TW',
    'كرواتي': 'hr',
    'دنماركي': 'da',
    'الماني': 'de',
    'انجليزي': 'en',
    'فنلندي': 'fil',
    'فرنسي': 'fr',
    'يوناني': 'el',
    'هنغاري': 'hu',
    'كوري': 'ko',
    'ايطالي': 'it',
    'ياباني': 'ja',
    'نرويجي': 'no',
    'بولندي': 'pl',
    'برتغالي': 'pt',
    'روسي': 'ru',
    'سلوفيني': 'sl',
    'اسباني': 'es',
    'سويدي': 'sv',
    'تركي': 'tr',
    'هندي': 'ur',
    'كردي': 'ku',
}

async def gtrans(text, lan):
    try:
        response = translate(text, lang_tgt=lan)
        if not response or not isinstance(response, (str, bytes)):
            return "تلقى استجابة غير صالحة من خدمة الترجمة"
        return response
    except Exception as er:
        return f"حدث خطأ \n{er}"

@l313l.ar_cmd(pattern="event")
async def handle_event(event):
    if event.reply_to_msg_id:
        m = await event.get_reply_message()
        with open("reply.txt", "w") as file:
            file.write(str(m))
        await event.client.send_file(event.chat_id, "reply.txt")
        os.remove("reply.txt")

@l313l.ar_cmd(
    pattern="ترجمة ([\s\S]*)",
    command=("ترجمة", "tools"),
    info={
        "header": "To translate the text to required language.",
        "note": "For language codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl en ; Catuserbot is one of the popular bot",
    },
)
async def translate_text(event):
    "To translate the text."
    input_str = event.pattern_match.group(1).strip()
    
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";", 1)
        lan = lan.strip()
        text = text.strip() if text else ""  # Ensure text is not None
    else:
        return await edit_delete(
            event, "** قم بالرد على الرسالة للترجمة **", time=5
        )
    
    text = soft_deEmojify(text) or ""  # Ensure text is not None

    try:
        trans = await gtrans(text, lan)
        if not trans:
            return await edit_delete(event, "**تحقق من رمز اللغة !, لا يوجد هكذا لغة**")      
        if isinstance(trans, str):
            output_str = f"**تمت الترجمة من ar الى {lan}**\n`{trans}`"
            await edit_or_reply(event, output_str)
        else:
            await edit_delete(event, f"**خطا:**\n`استجابة غير صالحة`", time=5)
    except Exception as exc:
        await edit_delete(event, f"**خطا:**\n`{exc}`", time=5)

@l313l.ar_cmd(pattern="(الترجمة الفورية|الترجمه الفوريه|ايقاف الترجمة|ايقاف الترجمه)")
async def toggle_translation(event):
    if gvarstatus("transnow"):
        delgvar("transnow")
        await edit_delete(event, "**✎┊‌ تم تعطيل الترجمه الفورية **")
    else:
        addgvar("transnow", "Reda") 
        await edit_delete(event, "**✎┊‌ تم تفعيل الترجمه الفورية**")

@l313l.ar_cmd(pattern="لغة الترجمة")
async def set_translation_language(event):
    t = event.text.replace(".لغة الترجمة", "").strip()
    try:  
        lang = langs[t]
    except KeyError:
        return await edit_delete(event, "**✎┊‌ !تأكد من قائمة اللغات. لا يوجد هكذا لغة**")
    addgvar("translang", lang)
    await edit_delete(event, f"**✎┊‌ تم تغير لغة الترجمة الى {lang} بنجاح ✓ **")

@l313l.on(events.NewMessage(outgoing=True))
async def auto_translate(event):
    if gvarstatus("transnow"):
        if event.media or isinstance(event.media, (types.MessageMediaDocument, types.MessageMediaInvoice)):
            print("JoKeRUB")
        else:
            original_message = event.message.message
            if original_message:
                lang = gvarstatus("translang") or "en"
                if lang:
                    translated_message = await gtrans(soft_deEmojify(original_message.strip()), lang)
                    if translated_message:
                        await event.message.edit(translated_message)
                    else:
                        await event.message.edit("حدث خطأ أثناء الترجمة.")
                else:
                    await event.message.edit("لم يتم تحديد لغة الترجمة.")
