from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🖋️ Edit photo', callback_data='edit')],
    [InlineKeyboardButton(text='🧠 Analyze image', callback_data='analysis')],
    [InlineKeyboardButton(text='📁 Compress/convert photo', callback_data='convert')]
])

edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔁 Resize', callback_data='resize')],
    [InlineKeyboardButton(text='🖌️ Retouch/enhance', callback_data='retouch')],
    [InlineKeyboardButton(text='🗑️ Remove background', callback_data='removebg')],
    [InlineKeyboardButton(text='🔙 Back', callback_data='back')]
])

analysis = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔡 Text recognition', callback_data='text')],
    [InlineKeyboardButton(text='👱 Face recognition', callback_data='face')],
    [InlineKeyboardButton(text='🧠 Photo analysis', callback_data='photo_analysis')],
    [InlineKeyboardButton(text='🔙 Back', callback_data='back')]
])

convert = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📂 Change format', callback_data='format')],
    [InlineKeyboardButton(text='🖼️ Compress photo', callback_data='compression')],
    [InlineKeyboardButton(text='🔙 Back', callback_data='back')]
])

format = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='PNG ↔ JPG', callback_data='PNGtoJPG')],
    [InlineKeyboardButton(text='JPG ↔ PNG', callback_data='JPGtoPNG')],
    [InlineKeyboardButton(text='WEBP ↔ PNG', callback_data='WEBPtoPNG')],
    [InlineKeyboardButton(text='WEBP ↔ JPG', callback_data='WEBPtoJPG')],
    [InlineKeyboardButton(text='🔙 Back', callback_data='BackToConvert')]
])
