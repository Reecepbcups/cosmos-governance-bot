# I do not know docker yet, but this worked. Will learn more soon to use w/ akash
# sudo docker build -t govbot:0.0.1 .
# sudo docker image ls
# sudo docker run <Id>

FROM python:latest

LABEL Maintainer="reecepbcups"

WORKDIR /usr/app/src

COPY . ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./GovBot.py"]
