from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import datetime

app = Flask(__name__)

# index -> main site view
@app.route("/")
def main():
    return render_template('index.html')

# home -> news and picture overview
@app.route("/home/")
def home():
    return render_template('home.html')

# about -> information of all people connected to this project
@app.route('/about/')
def about():
    return render_template('about.html')

# contact -> displayed contact information to support and developers
@app.route('/contact/')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.config['DEBUG'] = True
    ### for local testing uncomment first app.run and comment the other
    app.run(host='0.0.0.0', port=80)

    ### for deployment uncomment second app.run and comment the other
    # app.run(host='0.0.0.0')