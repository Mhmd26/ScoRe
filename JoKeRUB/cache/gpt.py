# gpt_module.py

import pytgpt.phind

# تهيئة بوت PHIND
bot = pytgpt.phind.PHIND()

def gpt(message):
    return bot.chat(message)
