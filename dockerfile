FROM python:3.11.6

WORKDIR /app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /src .

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD [wait-for-it db:5432 uvicorn main:app --host 0.0.0.0 --port 8000]
