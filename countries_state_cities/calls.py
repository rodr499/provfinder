import json
import os
import requests

class Region():
    
    root = os.path.dirname(os.path.abspath(__file__))

    def files(self, fileName):
        with open(self.root+"/"+fileName+".json", encoding="utf8") as jsonData:
            data = jsonData.read()

        return data

    def callCountry(self, country=None):
        countries = json.loads(self.files('countries'))

        countriesDict = {}
        for i in range(len(countries)):
            countriesDict[countries[i]['iso2']] = countries[i]['name']

        return countriesDict

    def callState(self, countryID):
        states = json.loads(self.files('states'))
        statesDict = {}
        for i in range(len(states)):
            if (states[i]['country_code'].upper() == countryID.upper()):
                statesDict[states[i]['state_code']] = states[i]['name']

        return statesDict

    def callCity(self, stateID):
        cities = json.loads(self.files('cities'))

        citiesDict = {}
        for i in range(len(cities)):
            if (cities[i]['state_code'] == stateID.upper()):
                citiesDict[cities[i]['name']] = cities[i]['name']

        return citiesDict

    # def remoteCities(self, hi):
    #     data = requests.get('https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/cities.json').json()
    #     with open(self.root+"/cities.json", 'w', encoding='utf-8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)