def media_type(message):
    # تحقق من أن message هو كائن يحتوي على media
    if hasattr(message, 'media'):
        media = message.media
        if hasattr(media, 'document'):
            # إذا كان هناك مستند، تحقق من نوع المحتوى
            content_type = media.document.mime_type if media.document.mime_type else ''
            if content_type.startswith('audio/'):
                return 'Audio'
            elif content_type.startswith('image/'):
                return 'Image'
            elif content_type.startswith('video/'):
                return 'Video'
            elif content_type.startswith('text/'):
                return 'Text'
            elif content_type.startswith('application/'):
                return 'Application'
            else:
                return 'Unknown'
        elif hasattr(media, 'photo'):
            # إذا كان هناك صورة
            return 'Image'
        elif hasattr(media, 'video'):
            # إذا كان هناك فيديو
            return 'Video'
        elif hasattr(media, 'audio'):
            # إذا كان هناك مقطع صوتي
            return 'Audio'
        else:
            return 'Unknown'
    else:
        # إذا لم يكن message يحتوي على media، ارجع 'Unknown'
        return 'Unknown'

# مثال على كيفية استخدام الدالة
class Message:
    def __init__(self, media):
        self.media = media

class Media:
    def __init__(self, mime_type=None):
        self.document = Document(mime_type)

class Document:
    def __init__(self, mime_type):
        self.mime_type = mime_type

# اختبار الدالة
reply = Message(Media('audio/mpeg'))
mediatype = media_type(reply)
print(mediatype)  # سيطبع 'Audio'
