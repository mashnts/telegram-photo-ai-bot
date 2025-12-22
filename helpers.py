from aiogram.types import Message
from io import BytesIO


async def get_photo_bytes(message: Message) -> bytes:
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)

    file_io = BytesIO()
    await message.bot.download_file(file.file_path, file_io)
    return file_io.getvalue()
