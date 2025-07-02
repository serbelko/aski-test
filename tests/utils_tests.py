from datetime import datetime
from unittest.mock import patch

from src.servises.utils import parse_d_field, get_yesterday_date, convert_date_to_russian_format


def test_parse_d_field_01():
    input_str = "2507021305"
    expected = "2025-07-02"
    assert parse_d_field(input_str) == expected


def test_convert_date_to_russian_format():
    input_date = "2024-12-31"
    expected = "31.12.2024"
    assert convert_date_to_russian_format(input_date) == expected


@patch("src.servises.utils.datetime")
def test_get_yesterday_date(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 7, 2)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    expected = "2025-07-01"
    assert get_yesterday_date() == expected