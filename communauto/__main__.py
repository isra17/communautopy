from haversine import haversine
from . import Client
client = Client()
proposals = client.get_vehicle_proposals(45.5393025, -73.5695876)
vehicle = proposals.closest
distance = haversine(vehicle.position, proposals.user_position)
print('Closest vehicle: {} at {:0.2f} km'.format(vehicle, distance))
