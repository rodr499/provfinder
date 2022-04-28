import json
import requests

class NPIregistry():

    def __init__(self, api, limit=10, **kwargs):
        self.api = api
        self.limit = limit
        self.kwargs = kwargs

    def apiURL(self):

        if (self.api == 1):
            apiURL = 'https://npiregistry.cms.hhs.gov/api/?version=2.1&' + str(self.limit) + '&'
        else:
            # This API with only work with CMS Order and Referring Dataset
            apiURL = 'https://data.cms.gov/data-api/v1/dataset/0824b6d0-14ad-47a0-94e2-f317a3658317/data?'
        
        return apiURL

    def fieldsBuilder(self):

        fields = []

        for k, v in self.kwargs.items():
            if (self.api == 1):
                fields.append(str(k)+'='+str(v))
            else:
                fields.append('filter['+(k)+']='+str(v))
        
        fields = '&'.join(fields)
    
        return fields

    def urlBuiler(self):

        apiURL = self.apiURL() + self.fieldsBuilder()

        return apiURL

    def requestDataset(self):

        data = requests.get(self.urlBuiler()).json()

        print(data)

        return data       

# NPIregistry(1,number=1356532162,).requestDataset()
# NPIregistry(2,NPI=1356532162).requestDataset()

"""
API 1

Descriptions of the fields that may be entered as criteria:

***** version: Identifies the version of the API to use (e.g., “2.0”, “2.1”). // The version has been hardcoded in this app.

number: The NPI Number is the unique 10-digit National Provider Identifier assigned to the provider.
enumeration_type: The Read API can be refined to retrieve only Individual Providers or Organizational Providers. When it is not specified, both Type 1 and Type 2 NPIs will be returned. When using the Enumeration Type, it cannot be the only criteria entered. Additional criteria must also be entered as well. Valid values are:
NPI-1: Individual Providers (Type 1) NPIs
NPI-2: Organizational Providers (Type 2) NPIs
taxonomy_description: Search for providers by their taxonomy by entering the taxonomy description.
first_name: This field only applies to Individual Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered (e.g. "jo*" ). This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.
use_first_name_alias (Version 2.1): This field only applies to Individual Providers when not doing a wildcard search. When set to "True", the search results will include Providers with similar First Names. E.g., first_name=Robert, will also return Providers with the first name of Rob, Bob, Robbie, Bobby, etc. Valid Values are:
True: Will include alias/similar names.
False: Will only look for exact matches.
Default Value is True
last_name: This field only applies to Individual Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered. This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.
organization_name: This field only applies to Organizational Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered. This field allows the following special characters: ampersand, apostrophe, "at" sign, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon. All types of Organization Names (LBN, DBA, Former LBN, Other Name) associated with an NPI are examined for matching contents, therefore, the results might contain an organization name different from the one entered in the Organization Name criterion.
address_purpose: Refers to whether the address information entered pertains to the provider's Mailing Address or the provider's Practice Location Address. When not specified, the results will contain the providers where either the Mailing Address or any of Practice Location Addresses match the entered address information. PRIMARY will only search against Primary Location Address. While Secondary will only search against Secondary Location Addresses. Valid values are:
LOCATION
MAILING
PRIMARY
SECONDARY
city: The City associated with the provider's address identified in Address Purpose. To search for a Military Address enter either APO or FPO into the City field. This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.
state: The State abbreviation associated with the provider's address identified in Address Purpose. This field cannot be used as the only input criterion. If this field is used, at least one other field, besides the Enumeration Type and Country, must be populated. Valid values for states.
postal_code (Version 2.0): The Postal Code associated with the provider's address identified in Address Purpose. There is an implied trailing wildcard. If you enter a 5 digit postal code, it will match any appropriate 9 digit (zip+4) codes in the data.
postal_code (Version 2.1): The Postal Code associated with the provider's address identified in Address Purpose. If you enter a 5 digit postal code, it will match any appropriate 9 digit (zip+4) codes in the data. Trailing wildcard entries are permitted requiring at least two characters to be entered (e.g., "21*").
country_code: The Country associated with the provider's address identified in Address Purpose. This field can be used as the only input criterion as long as the value selected is not US (United States). Valid values for countries.
limit: Limit the results returned. The default value is 10; however, the value can be set to any value from 1 to 200.
skip: The first N (value entered) results meeting the entered criteria will be bypassed and will not be included in the output.
pretty: When checked, the response will be displayed in an easy to read format. See NPPES Read API Examples.
NPPES Read API Output JSON Document
The Output of the Read API is a JSON document and it is made up of several data objects, some of which are either nested or contain arrays.

The Addresses array has two occurrences. The first address in the array will always be the Primary Practice Location and the second address in the array will always be the Mailing Address.
The Other Identifiers array contains up to 50 occurrences.
The Taxonomies array contains up to 15 occurrences.
The Other Names array may contain multiple Other Name occurrences.
The Endpoints will display in an array.
The Practice Locations array will contain all Practice Location Addresses except for the Primary Practice Location Address.

"""

"""
API 2
************ Access API for Order and Referring

NPI	NUMERIC
LAST_NAME	TEXT
FIRST_NAME	TEXT
PARTB	TEXT
DME	TEXT
HHA	TEXT
PMD	TEXT

"""