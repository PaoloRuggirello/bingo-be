FROM python:3.8-slim

WORKDIR /bingo/bingo-core
ADD ../bingo-core /bingo/bingo-core
WORKDIR /bingo/bingo-core
RUN pip install -r requirements.txt
RUN python3 setup.py sdist bdist_wheel

COPY bingo-be/requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD bingo-be /bingo/bingo-be

WORKDIR /bingo/bingo-be
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

