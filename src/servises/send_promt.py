import google.generativeai as genai
import re
import json
import logging
from config import config
from src.servises.db_func import get_organization_name, get_list_meetings, get_messages_from_tg
from src.servises.utils import get_yesterday_date

logger = logging.getLogger(__name__)


def get_daily_company_statistics_prompt(organization_id: str, date: str) -> str:
    organization_name = get_organization_name(organization_id)
    if organization_name is None:
        return "Index Error"
    meetings = get_list_meetings(organization_name, date)
    messages = get_messages_from_tg(organization_name, date)

    meetings_str = json.dumps(meetings, ensure_ascii=False, indent=2, default=str)
    messages_str = json.dumps(messages, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Ты — дружелюбный корпоративный ассистент. Каждый день ты составляешь тёплый, живой и понятный отчёт по активности команды за вчерашний день. Напиши приветствие, как будто общаешься с коллегами: можно добавить немного неформальности, смайлики, варьировать интонацию (не одинаковое начало каждый раз). После этого — краткая, но структурированная статистика.
Не используй никакого оформления Markdown, HTML и других. Пиши обычным текстом с необльшим количеством emoji.
Не нужно давить на участников, чтобы они начинали работать.
Выделяй только важные моменты работы, избегая лишних деталей.
Организация: {organization_name}  
Дата вчерашнего дня: {date}

Встречи:
{meetings_str}

Чаты:
{messages_str}

Сформируй отчёт по этой структуре:

👋 Приветствие дня: (не надо прописывать этот заголовок)
Например — “Доброе утро! Подведём итоги вчерашнего дня 👇” или “Доброго дня пятницы! Вот чем жила команда вчера:”. Не повторяйся каждый раз.

📊 Статистика:
- Количество встреч  
- Количество сообщений в чатах  
- Самые активные участники (по количеству сообщений)

🧠 Что обсуждали:
Сформулируй саммари по темам — кратко и по сути, чтобы коллеги могли быстро понять, о чём шла речь и какие были выводы.

🌟 Пожелание: (не надо прописывать этот заголовок)
Заверши отчёт коротким вдохновляющим пожеланием команде — с эмодзи, по-доброму, чтобы начать день с улыбки 😊

Если вчера не было активности (встреч и сообщений = 0), не пиши, что день был продуктивным. Вместо этого напиши что-то ободряющее, типа "Сегодня есть шанс сделать день особенным!" или "Вчера был тихий день — сегодня можно наверстать!"
Если была активность — можно хвалить и мотивировать: "Отличный ритм — продолжаем!" или "Хороший день, так держать!".

⚠️ Никаких JSON, никаких списков в скобках — только живой текст, структурированный заголовками. Не добавляй лишних пояснений. Пиши на русском.
"""
    return prompt


def get_gemini_answer(organization_id: str):
    """Возвращает ответ Gmini по указанной дате"""
    genai.configure(api_key=config.gpt_key.gpt_key)
    model = genai.GenerativeModel(model_name=config.gpt_key.model)
    prompt = get_daily_company_statistics_prompt(organization_id, get_yesterday_date())
    if prompt == 'Index Error':
        return 'Index Error'
    response = model.generate_content(prompt)
    return response.text


def get_gemini_answer_testing_date(organization_id: str, date: str):
    """Возвращает ответ Gmini по указанной дате"""
    genai.configure(api_key=config.gpt_key.gpt_key)
    model = genai.GenerativeModel(model_name=config.gpt_key.model)
    prompt = get_daily_company_statistics_prompt(organization_id, date)
    response = model.generate_content(prompt)
    return response.text

