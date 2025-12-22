from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from bot.states import ChatState, PhotoState, ConvertState
from bot.keyboards import main, edit, analysis, convert, format
from bot.services import start_chatting, analyze_photo, resize_image, enhance_image, compress_image, convert_image_format, remove_background, recognize_text_ocr, detect_faces
from helpers import get_photo_bytes

chat_router = Router()
photo_router = Router()

@chat_router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет!👋 Я ИИ бот🤖\n\n"
        "Доступные команды:\n"
        "🗣️ /conversation - начать диалог с AI\n"
        "🖼️ /options - работа с изображениями\n"
        "ℹ️ /help - помощь",
        reply_markup=main
    )

@chat_router.message(Command('options'))
async def options_command(message: Message):
    await message.answer("🖼️ Работа с изображениями:\nВыберите нужную функцию ниже:",
                        reply_markup=main)


@chat_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ Помощь по боту:\n\n"
        "📌 Команды:\n"
        "/start - главное меню\n"
        "/conversation - начать диалог с AI\n"
        "/options - работа с изображениями\n"
        "/stop - завершить диалог\n\n"
        "🖼️ Функции:\n"
        "• Чат с AI (DeepSeek)\n"
        "• Анализ фото с помощью GPT-4 Vision\n"
        "• Распознавание текста (OCR)\n"
        "• Распознавание лиц\n"
        "• Изменение размера изображений\n"
        "• Ретушь и улучшение качества\n"
        "• Удаление фона\n"
        "• Сжатие изображений\n"
        "• Конвертация форматов (PNG/JPEG/WEBP)"
    )


@chat_router.message(Command('conversation'))
async def handle_conversation(message: Message, state: FSMContext):
    await message.answer("Напишите стоп или /stop чтобы закончить диалог \n 🗣️ О чем поговорим?")
    await state.set_state(ChatState.chatting)


@chat_router.message(Command('stop'))
async def stop_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛑 Действие отменено\n\n"
        "/options - работа с изображениями\n"
        "/conversation - начать диалог снова"
    )


@chat_router.message(ChatState.chatting)
async def chat_mode(message: Message, state: FSMContext):
    if message.text and message.text.lower() in ("/stop", "стоп"):
        await state.clear()
        await message.answer(
            "🛑 Чат завершен\n\n"
            "/options - работа с изображениями\n"
            "/conversation - начать диалог снова"
        )
        return

    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    answer = await start_chatting(message.text)
    await message.reply(answer)


@photo_router.callback_query(F.data == 'edit')
async def edit_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "🖋️ Выберите тип редактирования:",
        reply_markup=edit
    )


@photo_router.callback_query(F.data == 'analysis')
async def analysis_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(
        "🧠 Выберите тип анализа:",
        reply_markup=analysis
    )


@photo_router.callback_query(F.data == 'convert')
async def convert_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📁 Выберите действие:",
        reply_markup=convert
    )


@photo_router.callback_query(F.data == 'photo_analysis')
async def photo_analysis_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖼️ Отправьте фотографию для анализа")
    await state.set_state(PhotoState.analysis)


@photo_router.callback_query(F.data == 'text')
async def text_recognition_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🔡 Отправьте фотографию с текстом для распознавания")
    await state.set_state(PhotoState.text)


@photo_router.callback_query(F.data == 'face')
async def face_recognition_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("👱 Отправьте фотографию для распознавания лиц")
    await state.set_state(PhotoState.face)


@photo_router.callback_query(F.data == 'resize')
async def resize_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🔁 Отправьте фотографию для изменения размера")
    await state.set_state(PhotoState.resize)


@photo_router.callback_query(F.data == 'retouch')
async def retouch_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖌️ Отправьте фотографию для ретуши")
    await state.set_state(PhotoState.retouch)


@photo_router.callback_query(F.data == 'removebg')
async def removebg_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🗑️ Отправьте фотографию для удаления фона")
    await state.set_state(PhotoState.rem_bg)


@photo_router.callback_query(F.data == 'format')
async def format_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📂 Выберите формат конвертации:",
        reply_markup=format
    )


@photo_router.callback_query(F.data.in_(['PNGtoJPG', 'JPGtoPNG', 'WEBPtoPNG', 'WEBPtoJPG']))
async def convert_format_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    conversion_map = {
        'PNGtoJPG': ('PNG', 'JPEG'),
        'JPGtoPNG': ('JPEG', 'PNG'),
        'WEBPtoPNG': ('WEBP', 'PNG'),
        'WEBPtoJPG': ('WEBP', 'JPEG')
    }

    source, target = conversion_map[callback.data]
    await callback.message.edit_text(f"📸 Отправьте изображение для конвертации в {target}")
    await state.set_state(ConvertState.image)
    await state.update_data(target_format=target)


@photo_router.callback_query(F.data == 'compression')
async def compression_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖼️ Отправьте фотографию для сжатия")
    await state.set_state(PhotoState.compression)


@photo_router.callback_query(F.data == 'back')
async def back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_text(
        "Привет!👋 Я ИИ бот🤖, что тебе подсказать?",
        reply_markup=main
    )


@photo_router.callback_query(F.data == 'BackToConvert')
async def back_to_convert_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📁 Выберите действие:",
        reply_markup=convert
    )


@photo_router.message(PhotoState.analysis)
async def analyze_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Анализирую изображение...")
    photo_bytes = await get_photo_bytes(message)
    answer = await analyze_photo(photo_bytes)

    await message.answer(answer)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)

@photo_router.message(PhotoState.text)
async def text_recognition_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Распознаю текст на изображении...")
    photo_bytes = await get_photo_bytes(message)
    result = await recognize_text_ocr(photo_bytes)

    await message.answer(f"📝 Распознанный текст:\n\n{result}")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(PhotoState.face)
async def face_recognition_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Распознаю лица на изображении...")
    photo_bytes = await get_photo_bytes(message)
    result = await detect_faces(photo_bytes)

    await message.answer(f"👤 Результат распознавания:\n\n{result}")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(PhotoState.resize)
async def resize_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Изменяю размер изображения...")
    photo_bytes = await get_photo_bytes(message)
    resized_bytes = await resize_image(photo_bytes, width=800)

    photo = BufferedInputFile(resized_bytes, filename="resized.png")
    await message.answer_photo(photo, caption="✅ Размер изменен до 800px по ширине")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(PhotoState.retouch)
async def retouch_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Ретуширую изображение...")
    photo_bytes = await get_photo_bytes(message)
    enhanced_bytes = await enhance_image(photo_bytes)

    photo = BufferedInputFile(enhanced_bytes, filename="enhanced.png")
    await message.answer_photo(photo, caption="✅ Изображение улучшено (резкость, контраст, цвета)")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(PhotoState.rem_bg)
async def remove_bg_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Удаляю фон с изображения...")
    photo_bytes = await get_photo_bytes(message)
    nobg_bytes = await remove_background(photo_bytes)

    photo = BufferedInputFile(nobg_bytes, filename="no_background.png")
    await message.answer_photo(photo, caption="✅ Фон удален")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(PhotoState.compression)
async def compression_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    await message.answer("⏳ Сжимаю изображение...")
    photo_bytes = await get_photo_bytes(message)

    original_size = len(photo_bytes) / 1024
    compressed_bytes = await compress_image(photo_bytes, quality=70)
    compressed_size = len(compressed_bytes) / 1024
    compression_ratio = ((original_size - compressed_size) / original_size) * 100

    photo = BufferedInputFile(compressed_bytes, filename="compressed.jpg")
    await message.answer_photo(
        photo,
        caption=f"✅ Изображение сжато\n"
                f"Исходный размер: {original_size:.1f} KB\n"
                f"Новый размер: {compressed_size:.1f} KB\n"
                f"Сжатие: {compression_ratio:.1f}%"
    )
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)


@photo_router.message(ConvertState.image)
async def convert_image_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, пришли именно фото 🖼️")
        return

    data = await state.get_data()
    target_format = data.get('target_format', 'PNG')

    await message.answer(f"⏳ Конвертирую в {target_format}...")
    photo_bytes = await get_photo_bytes(message)
    converted_bytes = await convert_image_format(photo_bytes, target_format)

    extension = 'jpg' if target_format == 'JPEG' else target_format.lower()
    photo = BufferedInputFile(converted_bytes, filename=f"converted.{extension}")
    await message.answer_photo(photo, caption=f"✅ Конвертировано в {target_format}")
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main)
