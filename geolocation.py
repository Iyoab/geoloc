import requests

API_KEY = 'AIzaSyAbd0ekZXpYV87FiN_taSW7gIV4zRzpN0k' #need an api key here

def get_address_from_user():
    address = input("Enter the address: ")
    return address

def get_lat_lon(address):
    params = {
        'key': API_KEY,
        'address': address
    }
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lon = geometry['location']['lng']
        return lat, lon
    else:
        return None, None

def main():
    address = get_address_from_user()
    lat, lon = get_lat_lon(address)
    if lat is not None and lon is not None:
        print("Latitude:", lat)
        print("Longitude:", lon)
    else:
        print("Error: Unable to retrieve coordinates for the provided address.")

if __name__ == "__main__":
    main()
