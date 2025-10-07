FROM python:3.11-slim

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["fastapi", "run","main.py","--host","0.0.0.0"]

