FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn","--workers", "3", "--timeout", "1000", "--bind", "0.0.0.0:8000"]

ENTRYPOINT ["gunicorn","Gem_mitra.wsgi"]