import numpy as np
import pandas as pd
import json
import os

class Sheet():

    root = os.path.dirname(os.path.abspath(__file__))
    

    def __init__(self,dataNPI):
        self.dataNPI = dataNPI
        self.data = pd.DataFrame(columns=self.grabColumns())

    def general_info(self,i,items):
        npiType = items["enumeration_type"]
        number = self.data.loc[i,"NPI"] = items["number"]
        self.data.loc[i,"Entity Type Code"] = npiType

        return npiType, number

    def basic(self,i,items,type):
        middleINIT = ""
        middleName = ""

        if "Replacement NPI" in items["basic"]:
            self.data.loc[i,"Replacement NPI"] = items["basic"]["replacement_npi"]

        if "ein" in items["basic"]:
            self.data.loc[i,"Employer Identification Number (EIN)"] = items["basic"]["ein"]

        if type != "NPI-2":
            
            if "middle_name" in items["basic"]:
                middleName = items["basic"]["middle_name"]
                if len(middleName) > 1:
                    middleINIT = middleName[0] + "."

            self.data.loc[i,"Full Name"] = items["basic"]["name"] 
            self.data.loc[i,"Last, First Middle"] = items["basic"]["last_name"] + ", " + items["basic"]["first_name"] + " " + middleName
            self.data.loc[i,"Last, First M."] = items["basic"]["last_name"] + ", " + items["basic"]["first_name"] + " " + middleINIT
            self.data.loc[i,"Provider Last Name (Legal Name)"] = items["basic"]["last_name"]
            self.data.loc[i,"Provider First Name"] = items["basic"]["first_name"]
            if "middle_name" in items["basic"]:
                self.data.loc[i,"Provider Middle Name"] = items["basic"]["middle_name"]
            if "name_prefix" in items["basic"]:
                self.data.loc[i,"Provider Name Prefix Text"] = items["basic"]["name_prefix"]
            if "name_suffix" in items["basic"]:
                self.data.loc[i,"Provider Name Suffix Text"] = items["basic"]["name_suffix"]
            if "credential" in items["basic"]:
                self.data.loc[i,"Provider Credential Text"] = items["basic"]["credential"]
        else:
            self.data.loc[i,"Provider Organization Name (Legal Business Name)"] = items["basic"]["organization_name"]

    def addresses(self,i,items,type):
        if "addresses" in items:
            for addresses in items["addresses"]:
                address_purpose = addresses["address_purpose"]
                address = f'{addresses["address_1"]} {addresses["address_2"]}, {addresses["city"]}, {addresses["state"]} {addresses["postal_code"]}'

                match address_purpose:
                    case "LOCATION":
                        self.data.loc[i,"Location Address"] = address
                    case "MAILING":
                        self.data.loc[i,"Mialing Address"] = address
                    case "PRIMARY":
                        self.data.loc[i,"Primary Address"] = address
                    case "SECONDARY":
                        self.data.loc[i,"Seconday Address"] = address

    def other_name(self,i,items,type):
        if "other_names" in items:
            for names in items["other_names"]:
                self.data.loc[i,"Provider Other Last Name"] = names["last_name"]
                self.data.loc[i,"Provider Other First Name"] = names["first_name"]
                self.data.loc[i,"Provider Other Middle Name"] = names["middle_name"]
                if "prefix" in items["other_names"]:
                    self.data.loc[i,"Provider Other Name Prefix Text"] = names["prefix"]
                if "suffix" in items["other_names"]:
                    self.data.loc[i,"Provider Other Name Suffix Text"] = names["suffix"]
                if "credential" in items["other_names"]:
                    self.data.loc[i,"Provider Other Credential Text"] = names["credential"]


    def taxonomies(self,i,items,type):
        if "taxonomies" in items:
            code_list = []
            statelicense_list = []
            state_list = []
            primary_list = []

            for tax in items["taxonomies"]:
                code_list.append(tax["code"])
                statelicense_list.append(tax["license"])
                state_list.append(tax["state"])
                primary_list.append(str(tax["primary"]))
            
            self.data.loc[i,"Healthcare Provider Primary Taxonomy"] = "\n".join(primary_list)
            self.data.loc[i,"Healthcare Provider Taxonomy"] = "\n".join(code_list)
            self.data.loc[i,"Provider License Number"] = "\n".join(statelicense_list)
            self.data.loc[i,"Provider License Number State"] = "\n".join(state_list)
            


    def identifiers(self,i,items,type):
        if "identifiers" in items:
            identifiers = []
            code_list = []
            state = []
            issuer = []

            for identifier in items["identifiers"]:
                identifiers.append(identifier["identifier"])
                code_list.append(identifier["code"])
                state.append(identifier["state"])
                issuer.append(identifier["issuer"])

            self.data.loc[i,"Other Provider Identifier"] = "\n".join(identifiers)
            self.data.loc[i,"Other Provider Identifier Type Code"] = "\n".join(code_list)
            self.data.loc[i,"POther Provider Identifier State"] = "\n".join(state)
            self.data.loc[i,"Other Provider Identifier Issuer"] = "\n".join(issuer)



    def endpoints(self,i,items,type):
        if "endpoints" in items:
            identifiers = []
            code_list = []
            state = []
            issuer = []

            for identifier in items["identifiers"]:
                identifiers.append(identifier["identifier"])
                code_list.append(identifier["code"])
                state.append(identifier["state"])
                issuer.append(identifier["issuer"])

            self.data.loc[i,"Endpoint Type Description"] = "\n".join(identifiers)
            self.data.loc[i,"Endpoint"] = "\n".join(code_list)
            self.data.loc[i,"Affiliation"] = "\n".join(state)
            self.data.loc[i,"Endpoint Description"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Legal Business Name"] = "\n".join(issuer)
            self.data.loc[i,"Use Code"] = "\n".join(issuer)
            self.data.loc[i,"Use Description"] = "\n".join(issuer)
            self.data.loc[i,"Other Use Description"] = "\n".join(issuer)
            self.data.loc[i,"Content Code"] = "\n".join(issuer)
            self.data.loc[i,"Content Description"] = "\n".join(issuer)
            self.data.loc[i,"Other Content Description"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Address Line One"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Address Line Two"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Address City"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Address State"] = "\n".join(issuer)
            self.data.loc[i,"Affiliation Address Postal Code"] = "\n".join(issuer)

    def practiceLocations(self,i,items,type):
        if "practiceLocations" in items:
            pass

    def generateSheet(self):
        d = self.dataNPI

        i = 1
        for items in d:
            item = items["results"][0]
            npiType = self.general_info(i,item)[0] 
            self.basic(i,item,npiType)
            self.addresses(i,item,npiType)
            self.other_name(i,item,npiType)
            self.taxonomies(i,item,npiType)
            self.identifiers(i,item,npiType)
            self.endpoints(i,item,npiType)
            self.practiceLocations(i,item,npiType)
            i = i + 1
        
        file = self.data.to_excel("test.xlsx", sheet_name="Providers",encoding="utf-8", index=False)

        return file

    def grabColumns(self):

        with open(self.root+"/"+"npi_columns.json", "r", encoding="utf8") as jsonColumns:
            column = json.loads(jsonColumns.read())
            columnList = []
            for i in range(len(column)):
                columnList.append(column[i]["header"])
            
        return columnList