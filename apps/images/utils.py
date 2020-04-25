import base64
from PIL import Image, ImageSequence
from io import BytesIO

from django.conf import settings


def convert_to_thumb(image):
    buffered = BytesIO()
    thumb = Image.open(BytesIO(base64.b64decode(image)))
    if thumb.format == 'GIF':
        frames = ImageSequence.Iterator(thumb)

        def thumbnails(frames):
            for frame in frames:
                thumbnail = frame.copy()
                thumbnail.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
                yield thumbnail

        frames = thumbnails(frames)
        om = next(frames)
        om.info = thumb.info
        om.save(
            buffered,
            save_all=True,
            append_images=list(frames),
            format=thumb.format
        )
    else:
        thumb.thumbnail(settings.THUMBNAIL_SIZE)
        thumb.save(buffered, format=thumb.format)

    return base64.b64encode(buffered.getvalue()).decode()
