from . import Client
client = Client()
for vehicle in client.get_vehicle_proposals(45.49834,-73.5727541).vehicles:
    import ipdb;ipdb.set_trace()
    print('{}: {}'.format(vehicle, vehicle.position))
