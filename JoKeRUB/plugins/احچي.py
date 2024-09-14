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
    
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        
    mediatype = media_type(reply)
    if not reply or (mediatype and mediatype not in ["Voice", "Audio"]):
        return await edit_delete(event, "`قم بالرد على رسالة أو مقطع صوتي لتحويله إلى نص.`")
    
    jepevent = await edit_or_reply(event, "`يجري تنزيل الملف...`")
    oggfi = await event.client.download_media(reply, Config.TEMP_DIR)
    await jepevent.edit("`يجري تحويل الكلام إلى نص....`")
    
    r = sr.Recognizer()
    ogg = oggfi.removesuffix('.ogg')
   
    AudioSegment.from_file(oggfi).export(f"{ogg}.wav", format="wav")
    user_audio_file = sr.AudioFile(f"{ogg}.wav")
    with user_audio_file as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language=lan)
    except sr.UnknownValueError:
        return await edit_delete(event, "**لا يوجد كلام في المقطع الصوتي**")
    except sr.RequestError as e:
        return await edit_delete(event, f"**!لا يوجد كلام في هذا المقطع الصوتي\n{e}**")
    
    end = datetime.now()
    ms = (end - start).seconds
    
    string_to_show = "**يقول : **`{}`".format(text)
    await jepevent.edit(string_to_show)
    
    # إزالة الملفات المؤقتة
    os.remove(oggfi)
    os.remove(f"{ogg}.wav")

def to_text(pic, api):
    try:
        output = api.ocr_file(open(pic, 'rb'))
    except Exception as e:
        return f"حدث الخطأ التالي:\n{e}"
    else:
        if output:
            return output
        else:
            return "حدث خطأ في النظام، حاول مجدداً"
    finally:
        os.remove(pic)

@l313l.ar_cmd(pattern="استخرج(?:\s|$)([\s\S]*)",
               command=("استخرج", plugin_category))
async def _(event):
    reply = await event.get_reply_message()
    lan = event.pattern_match.group(1).strip()
    
    if not reply:
        return await edit_delete(event, "**✎┊‌ قم بالرد على الصورة المراد استخراج النص منها**")
    
    pic_file = await event.client.download_media(reply, Config.TMP_DOWNLOAD_DIRECTORY)
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
