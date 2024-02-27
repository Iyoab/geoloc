import requests
from nrf24l01 import RF24

API_KEY = '' # Google Maps API key

# Set up NRF24L01 module
radio = RF24.RF24(RF24.RPI_V2_GPIO_P1_22, RF24.RPI_V2_GPIO_P1_24, RF24.BCM2835_SPI_SPEED_8MHZ)
pipes = [0xABCDABCD71, 0x544d52687C]

def setup_radio():
    radio.begin()
    radio.setRetries(15,15)
    radio.openWritingPipe(pipes[1])
    radio.stopListening()

def send_coordinates_to_drone(lat, lon):
    data = f"{lat},{lon}"
    radio.write(data.encode())
    print("Coordinates sent to drone:", data)

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
    address = input("Enter the address: ")
    lat, lon = get_lat_lon(address)
    if lat is not None and lon is not None:
        print("Latitude:", lat)
        print("Longitude:", lon)
        setup_radio()
        send_coordinates_to_drone(lat, lon)
    else:
        print("Error: Unable to retrieve coordinates for the provided address.")

if __name__ == "__main__":
    main()
