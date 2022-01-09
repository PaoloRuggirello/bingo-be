FROM python:3.8-slim

WORKDIR /bingo/bingo-be
ADD . /bingo/bingo-be
RUN pip install -r requirements.txt


WORKDIR /bingo/bingo-be
CMD [ "python3", "main.py"]