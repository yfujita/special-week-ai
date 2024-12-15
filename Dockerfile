FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/ .
COPY ./bin/command.sh .

ENV OUTPUT_PATH=/repo
RUN mkdir $OUTPUT_PATH

ENV RACE_ID=""
ENV SKIP_LATEST=""

CMD ["bash", "command.sh"]