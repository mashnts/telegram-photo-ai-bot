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
        "Hello! 👋 I am an AI bot 🤖\n\n"
        "Available commands:\n"
        "🗣️ /conversation - start a conversation with AI\n"
        "🖼️ /options - work with images\n"
        "ℹ️ /help - help",
        reply_markup=main
    )

@chat_router.message(Command('options'))
async def options_command(message: Message):
    await message.answer("🖼️ Image tools:\nChoose a feature below:",
                        reply_markup=main)


@chat_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ Bot help:\n\n"
        "📌 Commands:\n"
        "/start - main menu\n"
        "/conversation - start a conversation with AI\n"
        "/options - work with images\n"
        "/stop - end the conversation\n\n"
        "🖼️ Features:\n"
        "• AI chat (DeepSeek)\n"
        "• Photo analysis with GPT-4 Vision\n"
        "• Text recognition (OCR)\n"
        "• Face recognition\n"
        "• Image resizing\n"
        "• Retouching and quality enhancement\n"
        "• Background removal\n"
        "• Image compression\n"
        "• Format conversion (PNG/JPEG/WEBP)"
    )


@chat_router.message(Command('conversation'))
async def handle_conversation(message: Message, state: FSMContext):
    await message.answer("Type stop or /stop to end the conversation.\n🗣️ What would you like to talk about?")
    await state.set_state(ChatState.chatting)


@chat_router.message(Command('stop'))
async def stop_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛑 Action cancelled\n\n"
        "/options - work with images\n"
        "/conversation - start a new conversation"
    )


@chat_router.message(ChatState.chatting)
async def chat_mode(message: Message, state: FSMContext):
    if message.text and message.text.lower() in ("/stop", "stop"):
        await state.clear()
        await message.answer(
            "🛑 Chat ended\n\n"
            "/options - work with images\n"
            "/conversation - start a new conversation"
        )
        return

    if not message.text:
        await message.answer("Please send a text message.")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    answer = await start_chatting(message.text)
    await message.reply(answer)


@photo_router.callback_query(F.data == 'edit')
async def edit_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "🖋️ Choose an editing option:",
        reply_markup=edit
    )


@photo_router.callback_query(F.data == 'analysis')
async def analysis_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(
        "🧠 Choose an analysis option:",
        reply_markup=analysis
    )


@photo_router.callback_query(F.data == 'convert')
async def convert_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📁 Choose an action:",
        reply_markup=convert
    )


@photo_router.callback_query(F.data == 'photo_analysis')
async def photo_analysis_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖼️ Send a photo to analyze.")
    await state.set_state(PhotoState.analysis)


@photo_router.callback_query(F.data == 'text')
async def text_recognition_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🔡 Send a photo with text to recognize.")
    await state.set_state(PhotoState.text)


@photo_router.callback_query(F.data == 'face')
async def face_recognition_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("👱 Send a photo for face recognition.")
    await state.set_state(PhotoState.face)


@photo_router.callback_query(F.data == 'resize')
async def resize_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🔁 Send a photo to resize.")
    await state.set_state(PhotoState.resize)


@photo_router.callback_query(F.data == 'retouch')
async def retouch_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖌️ Send a photo to retouch.")
    await state.set_state(PhotoState.retouch)


@photo_router.callback_query(F.data == 'removebg')
async def removebg_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🗑️ Send a photo to remove its background.")
    await state.set_state(PhotoState.rem_bg)


@photo_router.callback_query(F.data == 'format')
async def format_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📂 Choose a conversion format:",
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
    await callback.message.edit_text(f"📸 Send an image to convert to {target}.")
    await state.set_state(ConvertState.image)
    await state.update_data(target_format=target)


@photo_router.callback_query(F.data == 'compression')
async def compression_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text("🖼️ Send a photo to compress.")
    await state.set_state(PhotoState.compression)


@photo_router.callback_query(F.data == 'back')
async def back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_text(
        "Hello! 👋 I am an AI bot 🤖 How can I help you?",
        reply_markup=main
    )


@photo_router.callback_query(F.data == 'BackToConvert')
async def back_to_convert_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        "📁 Choose an action:",
        reply_markup=convert
    )


@photo_router.message(PhotoState.analysis)
async def analyze_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Analyzing the image...")
    photo_bytes = await get_photo_bytes(message)
    answer = await analyze_photo(photo_bytes)

    await message.answer(answer)
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)

@photo_router.message(PhotoState.text)
async def text_recognition_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Recognizing text in the image...")
    photo_bytes = await get_photo_bytes(message)
    result = await recognize_text_ocr(photo_bytes)

    await message.answer(f"📝 Recognized text:\n\n{result}")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(PhotoState.face)
async def face_recognition_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Recognizing faces in the image...")
    photo_bytes = await get_photo_bytes(message)
    result = await detect_faces(photo_bytes)

    await message.answer(f"👤 Recognition result:\n\n{result}")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(PhotoState.resize)
async def resize_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Resizing the image...")
    photo_bytes = await get_photo_bytes(message)
    resized_bytes = await resize_image(photo_bytes, width=800)

    photo = BufferedInputFile(resized_bytes, filename="resized.png")
    await message.answer_photo(photo, caption="✅ Image resized to 800px wide.")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(PhotoState.retouch)
async def retouch_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Retouching the image...")
    photo_bytes = await get_photo_bytes(message)
    enhanced_bytes = await enhance_image(photo_bytes)

    photo = BufferedInputFile(enhanced_bytes, filename="enhanced.png")
    await message.answer_photo(photo, caption="✅ Image enhanced (sharpness, contrast, and colors).")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(PhotoState.rem_bg)
async def remove_bg_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Removing the image background...")
    photo_bytes = await get_photo_bytes(message)
    nobg_bytes = await remove_background(photo_bytes)

    photo = BufferedInputFile(nobg_bytes, filename="no_background.png")
    await message.answer_photo(photo, caption="✅ Background removed.")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(PhotoState.compression)
async def compression_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    await message.answer("⏳ Compressing the image...")
    photo_bytes = await get_photo_bytes(message)

    original_size = len(photo_bytes) / 1024
    compressed_bytes = await compress_image(photo_bytes, quality=70)
    compressed_size = len(compressed_bytes) / 1024
    compression_ratio = ((original_size - compressed_size) / original_size) * 100

    photo = BufferedInputFile(compressed_bytes, filename="compressed.jpg")
    await message.answer_photo(
        photo,
        caption=f"✅ Image compressed\n"
                f"Original size: {original_size:.1f} KB\n"
                f"New size: {compressed_size:.1f} KB\n"
                f"Compression: {compression_ratio:.1f}%"
    )
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)


@photo_router.message(ConvertState.image)
async def convert_image_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Please send a photo. 🖼️")
        return

    data = await state.get_data()
    target_format = data.get('target_format', 'PNG')

    await message.answer(f"⏳ Converting to {target_format}...")
    photo_bytes = await get_photo_bytes(message)
    converted_bytes = await convert_image_format(photo_bytes, target_format)

    extension = 'jpg' if target_format == 'JPEG' else target_format.lower()
    photo = BufferedInputFile(converted_bytes, filename=f"converted.{extension}")
    await message.answer_photo(photo, caption=f"✅ Converted to {target_format}.")
    await state.clear()
    await message.answer("Choose an action:", reply_markup=main)
