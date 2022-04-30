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
def findProvider():
    results = None
    error = None
    if req.method == 'POST':
        npiCheck = NPIValidation(req.form['search']).checkNPI()
        if npiCheck:
            results = NPIregistry(1,number=req.form['search']).requestDataset()
            pecosResults = NPIregistry(2,NPI=req.form['search']).requestDataset()
            print(pecosResults)
            if (results['result_count'] == 1):
                return render_template("results/providerPage.html", results=results['results'][0],pecos=pecosResults)
            else:
                results = NPIregistry(1,first_name=req.form['firstName'],last_name=req.form['lastName']).requestDataset()
                # pecosResults = NPIregistry(2,NPI=req.form['search']).requestDataset()
                print(results)
        else:
            flash('INVALID NPI', 'error')
            results = 'No!'
    
    return render_template("results/resultsTable.html", results=results, error=error)