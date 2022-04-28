from flask import Flask, render_template
from api.npiAPI import NPIregistry

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('/error/404.html')

@app.route("/")
def main():
    return render_template("main.html")