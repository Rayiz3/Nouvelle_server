FROM python:3.10.8-slim

LABEL fly_launch_runtime="flask"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .
COPY src ./src

EXPOSE 8080

CMD [ "python3", "app.py" ]
