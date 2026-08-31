from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_delete_keyboard(expenses):
    
    buttons = []
    
    for exp in expenses:
        button = InlineKeyboardButton(
            text=f"❌ {exp.amount}₴ - {exp.category}",
            callback_data=f"delete_{exp.id}"
        )
        buttons.append([button])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
