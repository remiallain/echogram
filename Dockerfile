FROM python:3-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app/src
ENTRYPOINT [ "python" ]
CMD [ "/app/src/main.py" ]
