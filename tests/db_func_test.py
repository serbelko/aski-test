import pytest
from unittest.mock import patch, MagicMock

from src.servises.db_func import (
    get_organization_name,
    get_list_meetings,
    get_messages_from_tg,
)


@patch("src.servises.db_func.get_collection")
def test_org_name_found(collection_mock):
    """Возвращается имя, если документ найден"""
    cursor_mock = MagicMock()
    cursor_mock.find.return_value = [{"name": "Aski"}]
    collection_mock.return_value = cursor_mock

    result = get_organization_name("aski_id")
    assert result == "Aski"


@patch("src.servises.db_func.get_collection")
def test_org_name_missing(collection_mock):
    """Если документов нет, возвращается None"""
    cursor_mock = MagicMock()
    cursor_mock.find.return_value = []
    collection_mock.return_value = cursor_mock

    result = get_organization_name("missing_id")
    assert result is None


@patch("src.servises.db_func.get_collection")
def test_meetings_list_empty(collection_mock):
    """Пустой список, когда встреч нет"""
    cursor_mock = MagicMock()
    cursor_mock.find.return_value = []
    collection_mock.return_value = cursor_mock

    meetings = get_list_meetings("Aski", "2025-07-01")
    assert meetings == []


@patch("src.servises.db_func.get_collection")
def test_meetings_list_nonempty(collection_mock):
    """Возвращается список встреч за дату"""
    sample = [{"meeting_id": "123", "organization": "Aski", "date": "2025-07-01"}]
    cursor_mock = MagicMock()
    cursor_mock.find.return_value = sample
    collection_mock.return_value = cursor_mock

    meetings = get_list_meetings("Aski", "2025-07-01")
    assert meetings == sample


@patch("src.servises.db_func.get_collection")
@patch("src.servises.db_func.parse_d_field")
def test_tg_messages_all_skipped(mocker_parse, collection_mock):
    """Когда нет документов или нет chat_content, возвращаем []"""
    # нет документов
    collection_mock.return_value.find.return_value = []
    assert get_messages_from_tg("Aski", "2025-07-02") == []

    # есть документ, но chat_content отсутствует или None
    docs = [{}, {"chat_content": None}]
    collection_mock.return_value.find.return_value = docs
    assert get_messages_from_tg("Aski", "2025-07-02") == []


@patch("src.servises.db_func.get_collection")
@patch("src.servises.db_func.parse_d_field")
def test_tg_messages_filter_and_errors(parse_mock, collection_mock):
    """Обработка ошибок, фильтрация по дате и отсутствия поля 'd'"""
    parse_mock.side_effect = lambda d: (
        "2025-07-02" if d == "ok" else (_ for _ in ()).throw(ValueError("wrong"))
    )
    msgs = [
        {"text": "no date field"},
        {"d": "fail"},
        {"d": "ok", "text": "correct"},
    ]
    collection_mock.return_value.find.return_value = [{"chat_content": msgs}]

    result = get_messages_from_tg("Aski", "2025-07-02")
    assert result == [{"d": "ok", "text": "correct"}]
