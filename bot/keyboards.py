from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🖋️Редактировать фото', callback_data='edit')],
    [InlineKeyboardButton(text='🧠Проанализировать изображение', callback_data='analysis')],
    [InlineKeyboardButton(text='📁Сжать/конвертировать фото', callback_data='convert')]
])

edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔁Изменение размера', callback_data='resize')],
    [InlineKeyboardButton(text='🖌️Ретушь/улучшение качества', callback_data='retouch')],
    [InlineKeyboardButton(text='🗑️Удаление фона', callback_data='removebg')],
    [InlineKeyboardButton(text='🔙Назад', callback_data='back')]
])

analysis = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔡Распознавание текста', callback_data='text')],
    [InlineKeyboardButton(text='👱Распознавание лиц', callback_data='face')],
    [InlineKeyboardButton(text='🧠Анализ фото', callback_data='photo_analysis')],
    [InlineKeyboardButton(text='🔙Назад', callback_data='back')]
])

convert = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📂Изменение разрешения', callback_data='format')],
    [InlineKeyboardButton(text='🖼️Сжатие фото', callback_data='compression')],
    [InlineKeyboardButton(text='🔙Назад', callback_data='back')]
])

format = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='PNG ↔ JPG', callback_data='PNGtoJPG')],
    [InlineKeyboardButton(text='JPG ↔ PNG', callback_data='JPGtoPNG')],
    [InlineKeyboardButton(text='WEBP ↔ PNG', callback_data='WEBPtoPNG')],
    [InlineKeyboardButton(text='WEBP ↔ JPG', callback_data='WEBPtoJPG')],
    [InlineKeyboardButton(text='🔙Назад', callback_data='BackToConvert')]
])
