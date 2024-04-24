FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn","-b","127.0.0.1:2525","-w","4", "app:app"]
