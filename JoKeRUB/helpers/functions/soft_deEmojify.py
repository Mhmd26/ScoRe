from langdetect import detect, DetectorFactory
from JoKeRUB.helpers.functions.functions import translate

DetectorFactory.seed = 0  # Ensures consistent language detection

async def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None

async def gtrans(text, lan=None):
    try:
        if lan is None:
            lan = await detect_language(text)
            if not lan:
                return "Error detecting language."
        
        response = translate(text, lang_tgt=lan)
        if response == 400:
            return "Error: Invalid language code."
    except Exception as er:
        return f"حدث خطأ \n{er}"
    return response

# Example usage
async def translate_message(text):
    translated = await gtrans(text)
    print(f"Translated message: {translated}")
