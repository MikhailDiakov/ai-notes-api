FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libpq-dev curl && \
    apt-get clean

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "asyncio"]
