from flask import Flask
from bingo.BingoPaper import BingoPaper

app = Flask(__name__)


@app.route("/")
def hello():
    bingo_paper = BingoPaper()
    result = ''
    for card in bingo_paper.cards:
        result += str(card) + '\n\n'
    return result


if __name__ == '__main__':
    app.run()