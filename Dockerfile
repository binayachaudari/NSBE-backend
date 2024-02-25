from ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3

RUN python3 --version

RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "easy_lease.wsgi:application"]

