import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    OPENAI_API_KEY: str = os.getenv("openai_api_key", "")
    REPLICATE_API_TOKEN: str = os.getenv("replicate_api_token", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("telegram_bot_token", "")

    OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1/chat/completions"

    CHAT_MODEL: str = "deepseek/deepseek-chat"
    VISION_MODEL: str = "openai/gpt-4o"

    MAX_TOKENS: int = 300

    def validate(self) -> None:
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("Отсутствует ключ telegram_bot_token")


settings = Settings()
