FROM python:3.9-slim-buster
WORKDIR /instagram_analytics_docker
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "-u", "manage.py", "runserver"]
