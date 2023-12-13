import random
import os
import requests
from urllib import response
import subprocess
from flask import Flask, render_template, abort, request

from QuoteEngine import Ingestor
from QuoteEngine import QuoteModel
from MemeEngine import MemeGenerator

app = Flask(__name__)

meme = MemeGenerator('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for file in quote_files:
        quotes += Ingestor.parse(file)

    quotes = [q for q in quotes if q is not None]

    images_path = "./_data/photos/dog/"

    for root, _, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    assert quote is not None
    path = meme.make_meme(img, quote.body, quote.author)
    print(path)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form['image_url']
    response = requests.get(image_url)

    local_img = f'temp{random.randint(0, 1000)}.png'
    with open(local_img, 'wb') as fid:
        fid.write(response.content)

    quote_body = request.form['body']
    quote_author = request.form['author']
    quote = QuoteModel(quote_body, quote_author)

    path = meme.make_meme(local_img, quote.body, quote.author)

    subprocess.run(['del', local_img], shell=True)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
