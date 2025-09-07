FROM python:3.13-alpine
LABEL authors="johan"

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "dev", "src/webapi.py"]

EXPOSE 8000