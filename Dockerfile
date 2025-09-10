FROM python:3.13-alpine
LABEL authors="johan"

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python api/dataimport.py && fastapi run api/webapi.py

EXPOSE 8000