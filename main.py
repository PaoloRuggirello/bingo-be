from flask import Flask
from dto.BingoPaperDTO import BingoPaperDTO
from bingo.BingoPaper import BingoPaper

app = Flask(__name__)


@app.route("/newBingoPaper")
def hello():
    bingo_paper = BingoPaper()
    return BingoPaperDTO(bingo_paper).toJSON()


if __name__ == '__main__':
    app.run()