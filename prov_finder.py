from flask import Flask, jsonify, render_template, request as req, url_for, flash, send_file
from sqlalchemy import true
from npiApi.npiAPI import NPIregistry
from npiApi.npiValidation import NPIValidation
from countries_state_cities.calls import Region
import secrets
import pdfkit
from urllib.parse import urlparse
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
from function import jobs

app = Flask(__name__)

class Config:

    SECRET_KEY = secrets.token_hex()
    JOBS =[{
        "id": "CleanFile1", 
        "func": jobs,
        'replace_existing': True,
        "trigger": "interval", 
        "seconds": 300
    }]

    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:///flask_context.db")
    }
    SCHEDULER_API_ENABLED = True 

@app.errorhandler(404)
def not_found(e):
    return render_template('/error/404.html',error=e)

@app.route("/", methods=['POST','GET'])
def main():
    countries = Region().callCountry()
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

        for k, v in results.items():
            if (k == 'Errors'):
                return not_found(v[0])
            elif (results['result_count'] != 0):
                return render_template("results/resultsTable.html", results=results)

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

@app.route("/print/<number>")
def printPage(number):

    results = NPIregistry(1,number=number).requestDataset()  
    pecosResults = NPIregistry(2,NPI=number).requestDataset()
      
    return render_template("results/print.html", results=results['results'][0],pecos=pecosResults)

@app.route('/pdfgen/<number>')
def pdfgen(number):
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    baseURL = urlparse(req.base_url)
    url = baseURL.hostname + url_for('printPage', number=number)
   
    fileName = 'providerFiles/'+number+'.pdf'
    
    pdfkit.from_url(url,fileName,configuration=config)


    return send_file(fileName)

if __name__ == "__main__":
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', port='80', debug=True)