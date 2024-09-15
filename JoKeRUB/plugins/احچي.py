import io
import os
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment

from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import reply_id
import ocrspace

plugin_category = "utils"

# قائمة اللغات
langs = {
    'عربي': 'ara',
    'بلغاري': 'bul',
    'صيني مبسط': 'chs',
    'صيني تقليدي': 'cht',
    'كرواتي': 'hrv',
    'دنماركي': 'dan',
    'ألماني': 'deu',
    'إنجليزي': 'eng',
    'فنلندي': 'fin',
    'فرنسي': 'fre',
    'يوناني': 'gre',
    'هنغاري': 'hun',
    'كوري': 'kor',
    'إيطالي': 'ita',
    'ياباني': 'jpn',
    'نرويجي': 'nor',
    'بولندي': 'pol',
    'برتغالي': 'por',
    'روسي': 'rus',
    'سلوفيني': 'slv',
    'إسباني': 'spa',
    'سويدي': 'swe',
    'تركي': 'tur',
}

@l313l.ar_cmd(pattern="احجي(?:\s|$)([\s\S]*)",
               command=("احجي", plugin_category))
async def _(event):
    "تحويل الكلام إلى نص."
    
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    lan = input_str.strip()
    
    if not lan:
        return await edit_delete(event, "يجب أن تضع اختصار اللغة المطلوبة")
    
    if not reply or media_type(reply) not in ["Voice", "Audio"]:
        return await edit_delete(event, "`قم بالرد على رسالة أو مقطع صوتي لتحويله إلى نص.`")
    
    jepevent = await edit_or_reply(event, "`يجري تنزيل الملف...`")
    audio_file = io.BytesIO(await event.client.download_media(reply))
    await jepevent.edit("`يجري تحويل الكلام إلى نص....`")
    
    r = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file, format="ogg")
    wav_file = io.BytesIO()
    audio.export(wav_file, format="wav")
    wav_file.seek(0)

    with sr.AudioFile(wav_file) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data, language=lan)
    except sr.UnknownValueError:
        return await edit_delete(event, "**لا يوجد كلام في المقطع الصوتي**")
    except sr.RequestError as e:
        return await edit_delete(event, f"**!لا يوجد كلام في هذا المقطع الصوتي\n{e}**")
    
    end = datetime.now()
    ms = (end - start).seconds
    
    string_to_show = "**يقول : **`{}`".format(text)
    await jepevent.edit(string_to_show)

@l313l.ar_cmd(pattern="استخرج(?:\s|$)([\s\S]*)",
               command=("استخرج", plugin_category))
async def _(event):
    reply = await event.get_reply_message()
    lan = event.pattern_match.group(1).strip()
    
    if not reply:
        return await edit_delete(event, "**✎┊‌ قم بالرد على الصورة المراد استخراج النص منها**")
    
    pic_file = io.BytesIO(await event.client.download_media(reply))
    if not pic_file:
        return await edit_delete(event, "**✎┊‌ قم بالرد على صورة**")
    
    api = ocrspace.API()
    if lan:
        try:
            lang = langs[lan]
            api = ocrspace.API(language=lang)
        except KeyError:
            return await edit_delete(event, "**✎┊‌ !لا توجد هذه اللغة**")
    
    await edit_or_reply(event, "**✎┊‌ يجري استخراج النص...**")
    text = to_text(pic_file, api)
    await edit_or_reply(event, text)

def to_text(pic, api):
    try:
        pic.seek(0)
        output = api.ocr_file(pic)
    except Exception as e:
        return f"حدث الخطأ التالي:\n{e}"
    else:
        if output:
            return output
        else:
            return "حدث خطأ في النظام، حاول مجدداً"
