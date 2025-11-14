FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя
RUN groupadd -r django -g 1000 && useradd -r -u 1000 -g django django

WORKDIR /app

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY ./backend .

# Меняем владельца
RUN chown -R django:django /app

USER django

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]