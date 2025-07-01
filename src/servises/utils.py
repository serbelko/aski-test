from datetime import datetime, timedelta

def parse_d_field(d: str) -> str:
    """Преобразует d-поле из 'YYMMDDhhmm' в 'YYYY-MM-DD' 
    используется для парса сообщений тг"""
    return datetime.strptime(d, "%y%m%d%H%M").strftime("%Y-%m-%d")


def get_yesterday_date() -> str:
    """Возвращает вчерашнюю дату в формате YYYY-MM-DD"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def convert_date_to_russian_format(date_str: str) -> str:
    """
    Преобразует дату из формата YYYY-MM-DD в формат DD.MM.YYYY
    используется для парса записей митов
    """
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")