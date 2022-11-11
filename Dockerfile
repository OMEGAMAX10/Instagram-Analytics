FROM python:3.9-slim-buster
WORKDIR /instagram_analytics_docker
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD python3 -u manage.py runserver 0.0.0.0:8000
