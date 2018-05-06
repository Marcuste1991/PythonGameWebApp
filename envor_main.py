from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint

app = Flask(__name__)

# index -> main site view
@app.route("/")
def index():
    return render_template('index.html')

# home -> news and picture overview
@app.route("/home/")
def home():
    return render_template('home.html')

# about -> information of all people connected to this project
@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    ### for local testing uncomment first app.run and comment the other
    # app.run(host='0.0.0.0', port=80)

    ### for deployment uncomment second app.run and comment the other
    app.run(host='0.0.0.0')
