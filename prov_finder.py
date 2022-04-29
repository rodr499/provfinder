from flask import Flask, render_template, request as req, url_for
from requests import request
from api.npiAPI import NPIregistry
from api.npiValidation import NPIValidation

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('/error/404.html')

@app.route("/", methods=['POST','GET'])
def main():
    
    if req.method == 'POST':
        print(req.form['search'])

    return render_template("main.html")

@app.route("/find", methods=['POST','GET'])
def findProvider():
    results = ""

    if req.method == 'POST':
        npiCheck = NPIValidation(req.form['search']).checkNPI()
        if npiCheck:
            results = NPIregistry(1,number=req.form['search']).requestDataset() 
        else:
            results = 'No!'
    
    return render_template("results/resultsTable.html", results=results)