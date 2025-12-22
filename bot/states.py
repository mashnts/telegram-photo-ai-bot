from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    chatting = State()


class PhotoState(StatesGroup):
    generate = State()
    analysis = State()
    text = State()
    face = State()
    rem_bg = State()
    retouch = State()
    resize = State()
    compression = State()


class ConvertState(StatesGroup):
    image = State()
