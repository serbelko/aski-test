# Тестовый проект для Aski

Привет!  
Это тестовый проект для отбора в команду Aski. Здесь реализован FastAPI-сервис, который собирает данные о встречах и сообщениях, а затем генерирует корпоративные отчёты с помощью Google Gemini.

## Что делает проект?

- Получает данные о встречах и сообщениях из MongoDB
- Генерирует отчёты с помощью Google Gemini

## Как запустить?

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/serbelko/aski-test.git
    cd for_aski
    ```

2. **Создайте файл `.env`** (или используйте пример `.env.disk`) и заполните своими данными:
    ```
    HOST=127.0.0.1
    PORT=8082
    DB_URL=<ваш-url-для-бд>
    DB_NAME=aski
    GEMINI_MODEL=gemini-2.5-flash
    GEMINI_KEY=<ваш-gpt-key>
    ```

3. **Запустите через Docker:**
    ```bash
    docker-compose up -d web
    ```
    Остановить:
    ```bash
    docker-compose down
    ```

4. **Или локально:**
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

## Примеры API

- `GET /ping` — проверка, что сервис работает
- `POST /process_chat/` — обработка чата, пример запроса:
    ```json
    {
      "chat_id": 123,
      "organization_id": "Aski"
    }
    ```

## Тесты

Запустить тесты можно так:
```bash
pytest
```
или через Docker:
```bash
docker-compose run --rm tests
```

## Структура

- `main.py` — запуск приложения
- `src/api/` — маршруты FastAPI
- `src/servises/` — бизнес-логика и интеграции
- `config/` — настройки и подключение к MongoDB, а также настройки виртуального окружения
- `tests/` — тесты

## Логи

Логи пишутся в файл `app.log`.

Также можно использовать docker для просмотра 
```bash
docker-compose logs -f web
```

---

Проект написан специально для тестового задания в Aski. Если есть вопросы — всегда на связи!
