from config import get_collection
from src.servises.utils import parse_d_field
from config import get_collection
from typing import List, Dict


def get_organization_name(organization_id: str):
    """Получить имя организации по айди"""
    cursor = get_collection('organization').find({'id': organization_id})
    try:
        name = list(cursor)[0]['name']
        return name
    except IndexError:
        print('Такой компании не существует')
        return None


def get_list_meetings(organization_name: str, date: str):
    """Получить список с запиьсю всех встреч за определённый день в Json-формате"""
    cursor = get_collection('organization').find({'organization': organization_name,
                                                  'date': date})
    return list(cursor)


def get_messages_from_tg(organization: str, date_str: str) -> List[Dict]:
    """Возвращает все сообщения из чатов для заданной организации и даты.
        Дата в формате YYYY-MM-DD"""
    collection = get_collection("telegram_chats")
    results = []

    cursor = collection.find({"organization": organization})
    for doc in cursor:
        chat_content = doc.get("chat_content") or []
        for msg in chat_content:
            if "d" in msg:
                try:
                    msg_date = parse_d_field(msg["d"])
                    if msg_date == date_str:
                        results.append(msg)
                except Exception as e:
                    print("Ошибка разбора даты:", e)
    return results