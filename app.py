# Import the necessary modules
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

from goose3 import Goose
import cohere

# Define the endpoint for the root URL path ("/")
@app.route("/", methods=("GET", "POST"))
def index():

    # Initialize variables for the article name and summary
    articleName = None
    summary = None

    if request.method == "POST":
        urll = request.form["animal"]

        # Use Goose to extract article information from the URL
        g = Goose()
        article = g.extract(url=urll)

        # Extract the article name and body
        articleName = article.title
        articleBody = article.cleaned_text

        
        # Use the Cohere API to summarize the article
        apiKey = os.getenv('COHERE_APIKEY', 'default_value')
        co = cohere.Client(apiKey)

        response = co.summarize( 
            text = articleBody,
            format='paragraph',
            temperature=0.4,
            model='summarize-xlarge', 
            length='long',
            extractiveness='medium'
        )

        # Store the summary in the summary variable
        summary = response.summary
                

    # Renders the HTML template with the article name and summary included.
    return render_template("index.html", result=articleName, result5 =summary, fullArticle= articleBody )     


