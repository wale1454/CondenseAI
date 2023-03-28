import os

# import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


from goose3 import Goose
import cohere

@app.route("/", methods=("GET", "POST"))
def index():

    articleName = None
    summary = None

    if request.method == "POST":
        urll = request.form["animal"]

        g = Goose()
        article = g.extract(url=urll)

        articleName = article.title
        articleBody = article.cleaned_text

        # Summary
        articleBody2 = articleBody.replace("\n", " ")
        apiKey = os.getenv('COHERE_APIKEY', 'default_value')

#         apiKey = 'INSERT-API-KEY'

        co = cohere.Client(apiKey)

        response = co.summarize( 
            text = articleBody,
            model='summarize-xlarge', 
            length='long',
            extractiveness='medium'
        )

        summary = response.summary
                


    return render_template("index.html", result=articleName, result5 =summary)     


