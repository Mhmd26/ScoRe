import base64
import asyncio
from datetime import datetime, timedelta
from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from JoKeRUB import l313l

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute, set_temporary_mute, remove_temporary_mute
from . import BOTLOG, BOTLOG_CHATID, get_user_from_event

plugin_category = "admin"
joker_users = []
joker_mute = "https://telegra.ph/file/396efcfa71389027e4f5c.jpg"
joker_unmute = "https://telegra.ph/file/f9adf9269eb7a5aa2f122.jpg"
#=================== الكـــــــــــــــتم ===================  #

@l313l.ar_cmd(pattern=f"كتم(?:\s|$)([\s\S]*)")
async def mutejep(event):
    await event.delete()
    if event.is_private:
        replied_user = await event.client.get_entity(event.chat_id)
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**✎┊‌ هـذا المسـتخـدم مڪتـوم . . سـابقـاً **"
            )
        if event.chat_id == l313l.uid:
            return await edit_delete(event, "**‌ ✎┊‌ لمـاذا تࢪيـد كتم نفسـك؟  **")
        if event.chat_id ==815010872:
            return await edit_delete(event, "**✎┊‌ دي . . لا يمڪنني كتـم مطـور السـورس  **")
        try:
            mute(event.chat_id, event.chat_id)
            joker_users.append(replied_user)
        except Exception as e:
            await event.edit(f"**- خطـأ **\n`{e}`")
        else:
            return await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption="**✎┊‌ تم ڪتـم الـمستخـدم  . . بنجـاح ✓**",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#كتــم_الخــاص\n"
                f"**- الشخـص  :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(
                event, "**✎┊‌ أنـا لسـت مشـرف هنـا ؟!! .**"
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == l313l.uid:
            return await edit_or_reply(event, "** ✎┊‌. لمـاذا تࢪيـد كتم نفسـك؟  **")
        if user.id == 7275336620:
            return await edit_or_reply(event, "**✎┊‌ دي . . لا يمڪنني كتـم مطـور السـورس  **")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "**✎┊‌ عــذراً .. هـذا الشخـص مكتــوم سـابقــاً هنـا**"
            )
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(
                    event,
                    "**✎┊‌ عــذراً .. هـذا الشخـص مكتــوم سـابقــاً هنـا**",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        try:
            mute(user.id, event.chat_id)
            joker_users.append(user)
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "**✎┊‌ عــذراً .. ليـس لديـك صـلاحيـة حـذف الرسـائل هنـا**",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "**✎┊‌ عــذراً .. ليـس لديـك صـلاحيـة حـذف الرسـائل هنـا**"
                )
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        if reason:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**✎┊‌ المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**- تـم كتمـه بنجـاح ✓**\n\n**- السـبب :** {reason}",
            )
        else:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**✎┊‌ المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**- تـم كتمـه بنجـاح ✓**\n\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكــتم\n"
                f"**الشخـص :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الدردشـه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )

@l313l.ar_cmd(pattern=f"كتم مؤقت(?:\s|$)([\s\S]*)")
async def temporary_mute(event):
    await event.delete()
    if event.is_private:
        await event.edit("**✎┊‌ لا يمكن استخدام هذا الأمر في المحادثات الخاصة**")
        return
    
    parts = event.message.text.split(maxsplit=2)
    if len(parts) < 3:
        return await event.edit("**✎┊‌ الاستخدام: كتم مؤقت <user_id> <minutes>**")
    
    user_id = int(parts[1])
    try:
        minutes = int(parts[2])
    except ValueError:
        return await event.edit("**✎┊‌ يرجى إدخال عدد صحيح من الدقائق**")
    
    if minutes <= 0:
        return await event.edit("**✎┊‌ يجب أن يكون عدد الدقائق أكبر من 0**")
    
    user = await event.client.get_entity(user_id)
    if user.id == l313l.uid:
        return await edit_or_reply(event, "**✎┊‌ لمـاذا تࢪيـد كتم نفسـك؟  **")
    if user.id == 7275336620:
        return await edit_or_reply(event, "**✎┊‌ دي . . لا يمڪنني كتـم مطـور السـورس  **")

    expiry = datetime.utcnow() + timedelta(minutes=minutes)
    try:
        set_temporary_mute(user.id, event.chat_id, expiry)
        joker_users.append(user)
        await event.client.send_file(
            event.chat_id,
            joker_mute,
            caption=f"**✎┊‌ تم كتم المستخدم {user.first_name} بنجاح ✓**\n**- المدة:** {minutes} دقيقة"
        )
    except Exception as e:
        await event.edit(f"**- خطـأ **\n`{e}`")
    
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#كتم_مؤقت\n"
            f"**- الشخـص  :** [{user.first_name}](tg://user?id={user.id})\n"
            f"**- المدة :** {minutes} دقيقة\n"
            f"**- الدردشـه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )

@l313l.on(events.NewMessage)
async def handle_forwarded(event):
    if event.fwd_from:
        if is_muted(event.sender_id, event.chat_id):
            await event.delete()

#=================== الغـــــــــــــاء الكـــــــــــــــتم ===================  #

@l313l.ar_cmd(pattern=f"(الغاء الكتم|الغاء كتم)(?:\s|$)([\s\S]*)")
async def unmutejep(event):
    await event.delete()
    if event.is_private:
        replied_user = await event.client.get_entity(event.chat_id)
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**✎┊‌ عــذراً .. هـذا الشخـص غيــر مكتــوم هنـا**"
            )
        try:
            unmute(event.chat_id, event.chat_id)
            joker_users.remove(replied_user)
        except Exception as e:
            await event.edit(f"**- خطـأ **\n`{e}`")
        else:
            await event.client.send_file(
                event.chat_id,
                joker_unmute,
                caption="**✎┊‌ تـم الغــاء كتــم الشخـص هنـا .. بنجــاح ✓**",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم\n"
                f"**- الشخـص :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
                joker_users.remove(user)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await edit_or_reply(
                event,
                "**✎┊‌ الشخـص غيـر مكـتـوم**",
            )
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        await event.client.send_file(
            event.chat_id,
            joker_unmute,
            caption=f"**✎┊‌ المستخـدم :** {_format.mentionuser(user.first_name ,user.id)} \n**- تـم الغـاء كتمـه بنجـاح ✓**",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم\n"
                f"**✎┊‌ الشخـص :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**✎┊‌ الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )

@l313l.ar_cmd(pattern=r"قائمة المكتومين")
async def show_muted_users(event):
    if len(joker_users) > 0:
        joker_list = "**✎┊‌ قائمة المستخدمين المكتومين:**\n"
        for i, user in enumerate(joker_users, start=1):
            joker_link = f"[{user.first_name}](tg://user?id={user.id})"
            joker_list += f"{i}. {joker_link}\n"
        await event.edit(joker_list)
    else:
        await event.edit("**✎┊‌ لا يوجد مستخدمين مكتومين حاليًا**")

@l313l.on(events.NewMessage(incoming=True))
async def watcher(event):
    muted_info = is_muted(event.sender_id, event.chat_id)
    if muted_info:
        if isinstance(muted_info, dict):
            expiry = muted_info.get("expiry")
            if expiry and datetime.utcnow() > expiry:
                remove_temporary_mute(event.sender_id, event.chat_id)
            else:
                await event.delete()
        else:
            await event.delete()
