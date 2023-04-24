FROM python:3.11-alpine
EXPOSE 8000

WORKDIR /nbp_app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt  /nbp_app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /nbp_app

ENTRYPOINT ["python3"]
CMD ["nbp_api/manage.py", "runserver", "0.0.0.0:8000"]

