FROM python:3.11-slim

WORKDIR /app

# Ставим зависимости
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт и запускаем
EXPOSE 8082
CMD ["python", "main.py"]