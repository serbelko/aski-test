import google.generativeai as genai
from config import init_mongo
import re
import json
from config import config
from src.servises.db_func import get_organization_name, get_list_meetings, get_messages_from_tg
from src.servises.utils import get_yesterday_date


def extract_json(text: str):
    """Переводит текстовый промт в формат json"""
    try:
        # Найти первую часть, похожую на JSON-массив
        json_like = re.search(r"\[\s*{.*}\s*]", text, re.DOTALL)
        if json_like:
            return json.loads(json_like.group())
        else:
            print("JSON-блок не найден")
            return None
    except json.JSONDecodeError as e:
        print("Ошибка при разборе JSON:", e)
        return None


def get_daily_company_statistics_prompt(organization_id: str, date: str) -> str:
    organization_name = get_organization_name(organization_id)
    meetings = get_list_meetings(organization_name, date)
    messages = get_messages_from_tg(organization_name, date)

    meetings_str = json.dumps(meetings, ensure_ascii=False, indent=2, default=str)
    messages_str = json.dumps(messages, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Ты аналитик компании. На основе записей встреч и сообщений в чатах за вчерашний день нужно составить структурированную статистику по деятельности организации.

Организация: {organization_name}

Дата: {date}

Встречи:
{meetings_str}

Чаты:
{messages_str}

Сформируй итоговый отчёт в JSON-формате со следующими полями:
[
  {{
    "date": "Дата отчёта",
    "organization": "Название организации",
    "total_meetings": "Количество встреч за день",
    "total_chat_messages": "Количество сообщений в чатах",
    "top_chat_participants": ["Имя1", "Имя2", "..."],
    "key_themes": ["Тема1", "Тема2", "..."],
    "summary": "Сводка ключевых событий и обсуждений в течение дня"
  }}
]

Только JSON, без пояснений.
"""
    return prompt



def get_gemini_answer(organization_id: str):
    """Возвращает ответ Gmini по указанной дате"""
    init_mongo()
    genai.configure(api_key=config.gpt_key.gpt_key)
    model = genai.GenerativeModel(model_name=config.gpt_key.model)
    prompt = get_daily_company_statistics_prompt(organization_id, get_yesterday_date())
    response = model.generate_content(prompt)
    return extract_json(response.text)


def get_gemini_answer_testing_date(organization_id: str, date: str):
    """Возвращает ответ Gmini по указанной дате"""
    init_mongo()
    genai.configure(api_key=config.gpt_key.gpt_key)
    model = genai.GenerativeModel(model_name=config.gpt_key.model)
    prompt = get_daily_company_statistics_prompt(organization_id, date)
    response = model.generate_content(prompt)
    return extract_json(response.text)

