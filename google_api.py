
@app.route('/display_event') #put in the actual route
def maps(id):
    this_event = event.Event.get_evetn_by_id(id)

params = {
    'address' : this_event.location,
    'key': api_key
}
url_params = urlencode(params)
endpoint= f"https://maps.googleapis.com/maps/api/geocode/json?address={}"




