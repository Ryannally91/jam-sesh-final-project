import requests
from urllib.parse import urlencode
from google_api_key import api_key
import json

#hide later and import

base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
location = 'Zilker Park'
params = {
    "key": api_key,
    "input": {location},
    "inputtype": "textquery",
    "fields": "place_id,formatted_address,name,geometry"
}

params_encoded = urlencode(params)
places_endpoint = f"{base_url}?{params_encoded}"

r = requests.get(places_endpoint)
print(r.status_code)
print(r)
print(r.json())
r = r.json()
print('<><><>', r['candidates'])
print('^^^^^^^^^^^^',r['candidates'][0]['place_id'])
# py_r =json.loads(r)

# print(py_r.candidates[0].place_id)

#Everything works and prints json

# print(r.candidates[0].place_id) 



#How to embed map
# https://developers.google.com/maps/documentation/embed/get-started
#map code to putinHTML (user place_id to generate map display)
#<iframe width="600" height="450" style="border:0" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ22j54Ia1RIYRunKXejw_UJs&key=AIzaSyDiuDwsqOke9BM1-IIHO3Po4Djx3znCfqs"></iframe>


#This can be applied to create event, user registration (at least partly)
def parse_location(data):
        location_breakdown = data['location'].split(',')
        print(location_breakdown)
        data = {
            'location' : location_breakdown[:-3],
            'city' : location_breakdown[-3],
            'state' : location_breakdown[-2]
        }
        print(data)
        return data

data = {
    'location' : 'opa, Zilker, Austin, TX, USA'
}

parse_location(data)