import re
from flask import Flask, render_template, request as req, url_for, flash
from api.npiAPI import NPIregistry
from api.npiValidation import NPIValidation
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()

@app.errorhandler(404)
def not_found(e):
    return render_template('/error/404.html')

@app.route("/", methods=['POST','GET'])
def main():
    return render_template("main.html")

@app.route("/find", methods=['POST','GET'])
def viewProvider():
    results = None
    error = None

    if req.method == 'POST':
        npiCheck = NPIValidation(req.form['number']).checkNPI()
        if npiCheck:
            results = NPIregistry(1,number=req.form['number'],first_name='',last_name='').requestDataset()  
            if (results['result_count'] == 1):
                pecosResults = NPIregistry(2,NPI=results['results'][0]['number']).requestDataset()
                print(len(pecosResults))
                return render_template("results/providerPage.html", results=results['results'][0],pecos=pecosResults)
        else:
            flash('INVALID NPI', 'error')
            results = 'No!'
    return render_template("results/resultsTable.html", results=results, error=error)