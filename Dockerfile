FROM python:3.11

WORKDIR /dzen_code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd --create-home userapi

COPY . /dzen_code

RUN pip install --no-cache-dir -r requirements.txt

RUN python dzen_code/manage.py makemigrations
RUN python dzen_code/manage.py migrate

USER userapi
EXPOSE 8000

CMD ["python", "dzen_code/manage.py", "runserver", "0.0.0.0:8000"]
