from googlemaps import Client
API_KEY = 'AIzaSyCmDerOT1BmeDB-M3cHa_Tnm_aT4nLyQEc'
client = Client(key=API_KEY)

class Location:
    def __init__(self, position, description):
        self.position = position
        self.description = description

    @classmethod
    def search(cls, terms):
        locations = []
        geocodes = client.geocode(terms)
        for geocode in geocodes:
            coord = (geocode['geometry']['location']['lat'], geocode['geometry']['location']['lng'])
            location = cls(coord, geocode['formatted_address'])
            locations.append(location)
        return locations

    @classmethod
    def locate(cls):
        location = client.geolocate()

        coord = (location['location']['lat'], location['location']['lng'])
        geocode = client.reverse_geocode(latlng=location['location'])[0]
        coord = (geocode['geometry']['location']['lat'], geocode['geometry']['location']['lng'])
        location = cls(coord, geocode['formatted_address'])
        return location

    @classmethod
    def from_coord(cls, coord):
        geocode = client.reverse_geocode(latlng=coord)[0]
        coord = (geocode['geometry']['location']['lat'], geocode['geometry']['location']['lng'])
        location = cls(coord, geocode['formatted_address'])
        return location

    def __str__(self):
        return self.description

def distances(origin, destinations, mode='walking'):
    distances = client.distance_matrix(origins=origin, destinations=destinations, mode=mode, units='metric')
    return [{'address': a, **r} for r, a in zip(distances['rows'][0]['elements'], distances['destination_addresses'])]
