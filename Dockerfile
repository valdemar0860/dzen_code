FROM python:3.11

WORKDIR /dzen_code
RUN useradd --create-home userapi

COPY . /dzen_code
RUN pip install --no-cache-dir -r requirements.txt

#RUN django-admin startproject dzen_code .
#RUN python manage.py makemigrations
#RUN python manage.py migrate

USER userapi
EXPOSE 8000

CMD ["python", "dzen_code/manage.py", "runserver", "0.0.0.0:8000"]
