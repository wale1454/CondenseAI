import os

# import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# openai.api_key = "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"



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
        apiKey = 'INSERT-API-KEY'

        co = cohere.Client(apiKey)

        response = co.summarize( 
            text = articleBody,
            model='summarize-xlarge', 
            length='long',
            extractiveness='medium'
        )

        summary = response.summary
                


    return render_template("index.html", result=articleName, result5 =summary)     


