FROM python:3.8-slim-buster

COPY requirements.txt ./
# RUN python -m pip install flask redis
# RUN python -m pip freeze > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .