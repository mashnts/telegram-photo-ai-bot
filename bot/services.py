import base64, aiohttp
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from config import settings

async def start_chatting(user_text: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "HTTP-Referer": "PhotoAI_bot",
                    "X-Title": "telegram-chat-bot"
                },
                json={
                    "model": settings.CHAT_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты помощник в Telegram боте. Отвечай простым текстом без форматирования markdown (без **, __, `, [], () для ссылок). Используй только обычный текст и эмодзи."
                        },
                        {"role": "user", "content": user_text}
                    ],
                    "max_tokens": settings.MAX_TOKENS
                }
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при обращении к AI: {str(e)}"


async def analyze_photo(photo_bytes: bytes) -> str:
    try:
        base64_image = base64.b64encode(photo_bytes).decode()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "HTTP-Referer": "PhotoAI_bot",
                    "X-Title": "telegram-image-analyzer"
                },
                json={
                    "model": settings.VISION_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": "Проанализируй это изображение"
                                }
                            ]
                        }
                    ],
                    "max_tokens": settings.MAX_TOKENS
                }
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при анализе изображения: {str(e)}"

async def resize_image(photo_bytes: bytes, width: int = 800) -> bytes:
    img = Image.open(BytesIO(photo_bytes))
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)

    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    output = BytesIO()
    img_resized.save(output, format='PNG')
    return output.getvalue()

async def enhance_image(photo_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(photo_bytes))

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)

    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


async def compress_image(photo_bytes: bytes, quality: int = 70) -> bytes:
    img = Image.open(BytesIO(photo_bytes))

    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()


async def convert_image_format(photo_bytes: bytes, target_format: str) -> bytes:
    img = Image.open(BytesIO(photo_bytes))

    # для JPEG нужен RGB вместо RGBA
    if target_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[-1])
            img = background

    output = BytesIO()
    img.save(output, format=target_format.upper())
    return output.getvalue()


async def remove_background(photo_bytes: bytes) -> bytes:
    try:
        base64_image = base64.b64encode(photo_bytes).decode()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.remove.bg/v1.0/removebg",
                headers={"X-Api-Key": settings.REPLICATE_API_TOKEN},
                data={"image_file_b64": base64_image, "size": "auto"}
            ) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    return await simple_background_removal(photo_bytes)
    except:
        return await simple_background_removal(photo_bytes)


async def simple_background_removal(photo_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(photo_bytes)).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


async def recognize_text_ocr(photo_bytes: bytes) -> str:
    try:
        base64_image = base64.b64encode(photo_bytes).decode()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "HTTP-Referer": "PhotoAI_bot",
                    "X-Title": "telegram-ocr"
                },
                json={
                    "model": settings.VISION_MODEL,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                            {"type": "text", "text": "Распознай и выведи весь текст, который есть на этом изображении. Выведи только текст, без дополнительных комментариев."}
                        ]
                    }],
                    "max_tokens": 1000
                }
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при распознавании текста: {str(e)}"


async def detect_faces(photo_bytes: bytes) -> str:
    try:
        base64_image = base64.b64encode(photo_bytes).decode()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "HTTP-Referer": "PhotoAI_bot",
                    "X-Title": "telegram-face-detection"
                },
                json={
                    "model": settings.VISION_MODEL,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                            {"type": "text", "text": "Найди и опиши всех людей на этом изображении: сколько людей, их примерный возраст, пол, эмоции, что делают. Если людей нет, так и напиши."}
                        ]
                    }],
                    "max_tokens": 500
                }
            ) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при распознавании лиц: {str(e)}"
