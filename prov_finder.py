from unittest import result
from flask import Flask, jsonify, render_template, request as req, url_for, flash
from npiApi.npiAPI import NPIregistry
from npiApi.npiValidation import NPIValidation
from countries_state_cities.calls import Region
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()

@app.errorhandler(404)
def not_found(e):
    return render_template('/error/404.html')

@app.route("/", methods=['POST','GET'])
def main():

    countries = Region().callCountry()

    print(req.form.get('country_code'))

    if (req.method == 'POST'):

        country_code =str(req.form.get('country_code') or '')
        city=str(req.form.get('city') or '')
        state=str(req.form.get('state') or '')

        results = NPIregistry(1,first_name=req.form['first_name'],last_name=req.form['last_name'],
        organization_name=req.form['organization_name'],country_code=country_code,city=city,state=state,
        postal_code=req.form['postal_code']).requestDataset()

        resultsUrl = NPIregistry(1,first_name=req.form['first_name'],last_name=req.form['last_name'],
        organization_name=req.form['organization_name'],country_code=country_code,city=city,state=state,
        postal_code=req.form['postal_code']).urlBuiler()
        
        print(results)
        print(resultsUrl)
        return render_template("main.html", countries=countries, results=result)

    return render_template("main.html", countries=countries)

@app.route("/find", methods=['POST','GET'])
def viewProvider():
    results = None
    error = None

    if (req.method == 'POST'):
        npiCheck = NPIValidation(req.form['number']).checkNPI()
        if npiCheck:
            results = NPIregistry(1,number=req.form['number'],first_name='',last_name='').requestDataset()  
            if (results['result_count'] == 1):
                pecosResults = NPIregistry(2,NPI=results['results'][0]['number']).requestDataset()
                return render_template("results/providerPage.html", results=results['results'][0],pecos=pecosResults)
        else:
            flash('INVALID NPI', 'error')
            results = 'No!'
    return render_template("results/resultsTable.html", results=results, error=error)

@app.route("/provider/<int:number>")
def provider(number):

    results = NPIregistry(1,number=number).requestDataset()  
    pecosResults = NPIregistry(2,NPI=number).requestDataset()
      
    return render_template("results/providerPage.html", results=results['results'][0],pecos=pecosResults)

@app.route("/search", methods=['POST','GET'])
def search():
    results = None

    if (req.method == 'POST'):

        country_code =str(req.form.get('country_code') or '')
        city=str(req.form.get('city') or '')
        state=str(req.form.get('state') or '')

        results = NPIregistry(1,limit=60,first_name=req.form['first_name'],last_name=req.form['last_name'],
        organization_name=req.form['organization_name'],country_code=country_code,city=city,state=state,
        postal_code=req.form['postal_code']).requestDataset()
    
    
    return render_template("results/resultsTable.html", results=results)

@app.route("/regions/<type>/<rid>")
def regions(type, rid):
    results = None

    if (type == 'state'):
        results = Region().callState(rid)
    elif (type == 'city'):
        results = Region().callCity(rid)
    
    return jsonify(results)

@app.route("/c")
def credit():
    return render_template("misc/credits.html")