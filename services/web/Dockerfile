FROM python:3.10-bookworm

WORKDIR /app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]