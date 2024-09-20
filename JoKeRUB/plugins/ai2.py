from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from telethon import Button

@l313l.on(admin_cmd(pattern="26(?: |$)(.*)"))
async def _(event):
    # Sending the welcome message
    welcome_message = (
        "[𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗚𝗣𝗧 | 𝗚𝗲𝗺𝗶𝗻𝗶](t.me/Scorpion_scorp)\n\n**✎┊‌ اهلا وسهلا بك في قسم الذكاء الاصطناعي \nالخاص بسورس العقرب 🤖 **\n\n**✎┊ يمكن تشغيله من خلال ارسال** { `.سؤال` } **بلاضافة الى سؤالك وسيتم الرد عليك بعد بضع ثوانٍ\n\n و يمكنك الذهاب مباشره الى دردشة الذكاء لمعرفة الاصدارات الاخرى ✓‌**"
    )
    
    # Creating the button for subscribing
    buttons = [
        [Button.url("اشتراك في القناة", "https://t.me/Scorpion_scorp")]
    ]
    
    # Sending the message with the button, and disabling the link preview
    await event.client.send_message(
        event.chat_id,
        welcome_message,
        buttons=buttons,
        link_preview=False  # Disable link preview
    )
