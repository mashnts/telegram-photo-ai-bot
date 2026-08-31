from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from database import SessionLocal, get_or_create_user, add_expense, get_user_expenses, delete_expense, get_expenses_by_category

from keyboards import get_delete_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    session = SessionLocal()

    user = get_or_create_user(session, 
        telegram_id=message.from_user.id,
        username=message.from_user.username)
    
    session.close()

    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе вести учёт расходов\n\n"
        "📝 Просто пиши сумму и категорию:\n"
        "Например: <b>100 еда</b>\n\n"
        "Команды:\n"
        "/history - последние расходы\n"
        "/categories - расходы по категориям\n"
        "/delete - удалить расход\n",
        parse_mode="HTML"
    )


@router.message(Command("history"))
async def cmd_history(message: Message):
    session = SessionLocal()

    user = get_or_create_user(session, message.from_user.id, message.from_user.username)

    expenses = get_user_expenses(session, user.id, limit=10)

    if not expenses:
        await message.answer("Нет расходов!")
        session.close()
        return

    text = "📊 Последние расходы:\n\n"
    for exp in expenses:
        date_str = exp.date.strftime("%d.%m.%Y %H:%M")
        text += f"• {exp.amount}₴ — {exp.category}\n  {date_str}\n\n"
    
    session.close()
    await message.answer(text)


@router.message(Command("categories"))
async def cmd_category(message: Message):
    session = SessionLocal()

    user = get_or_create_user(session, message.from_user.id, message.from_user.username)

    expenses_by_category = get_expenses_by_category(session, user.id)
    session.close()
    
    if not expenses_by_category:
        await message.answer("Нет расходов!")
        return
    
    text = "📊 Расходы по категориям:\n\n"
    for category, total in expenses_by_category:
        text += f"• {category}: {total}₴\n"

    await message.answer(text)
        

@router.message(Command("delete"))
async def cmd_delete(message: Message):
    session = SessionLocal()
    user = get_or_create_user(session, message.from_user.id, message.from_user.username)
    expenses = get_user_expenses(session, user.id)
    session.close()

    if not expenses:
        await message.answer("Нет расходов для удаления!")
        return

    await message.answer(
        "Выберите расход для удаления:",
        reply_markup=get_delete_keyboard(expenses)
    )


@router.callback_query(F.data.startswith("delete_"))
async def callback_delete(callback: CallbackQuery):
    expense_id = int(callback.data.split("_")[1])

    session = SessionLocal()
    result = delete_expense(session, expense_id)
    session.close()

    if result:
        await callback.message.edit_text("Расход удалён!")
    else:
        await callback.message.edit_text("Расход не найден.")

    await callback.answer()


@router.message(F.text)
async def add_expense_handler(message: Message):
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    
    if len(parts) != 2:
        await message.answer("❌ Неправильный формат!\nПример: 100 еда")
        return
    
    amount_str, category = parts
    
    try:
        amount = float(amount_str)
    except ValueError:
        await message.answer("❌ Сумма должна быть числом!\nПример: 100 еда")
        return
    
    session = SessionLocal()
    user = get_or_create_user(session, message.from_user.id, message.from_user.username)
    
    expense = add_expense(session, user.id, amount, category)
    
    session.close()
    
    await message.answer(f"✅ Добавлено: {amount}₴ — {category}")


