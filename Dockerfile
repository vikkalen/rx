FROM arm32v6/python:3.7-alpine
WORKDIR /usr/src/rx
RUN pip install --no-cache-dir pyserial requests

COPY . .
CMD [ "python", "./rx.py" ]
