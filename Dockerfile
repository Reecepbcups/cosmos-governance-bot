# sudo docker build -t cosmos-gov-bot:2.0.2 .
# sudo docker run -it --rm --name gov-bot cosmos-gov-bot:2.0.2

FROM python:3-alpine

LABEL Maintainer="reecepbcups"

WORKDIR /usr/app/src

COPY requirements/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/gov-bot.py"]
