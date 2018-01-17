from haversine import haversine
from .utils import camel_to_snake, parse_date

class Model:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, camel_to_snake(k), v)


class Proposals(Model):
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self._client = client
        self.user_position = (self.user_position['Lat'], self.user_position['Lon'])
        vehicles = [Vehicle(self._client, **v) for v in self.vehicules]
        self.vehicles = list(sorted(vehicles, key=lambda v: haversine(v.position, self.user_position)))
        del self.vehicules

    def __repr__(self):
        return '<Proposals user_position={}, vehicles=<{} Vehicles>>'.format(self.user_position, len(self.vehicles))


class Vehicle(Model):
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self._client = client
        self.position = (self.position['Lat'], self.position['Lon'])

    def __repr__(self):
        return '<Vehicle id="{}", name="{}">'.format(self.id, self.name)

class Login(Model):
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self._client = client
        self._current_booking = None

    @property
    def current_booking(self, use_cache=True):
        if use_cache and self._current_booking:
            return self._current_booking
        self._current_booking = self._client.get_current_booking(self.provider_no)
        return self._current_booking

    def book(self, vehicle):
        self._current_booking = None
        return self._client.create_booking(self.provider_no, vehicle.id)

    def cancel_booking(self):
        current_booking = self.current_booking
        self._current_booking = None
        return self._client.cancel_booking(self.provider_no, current_booking.vehicle.id)

    def __repr__(self):
        return '<Login customer_id="{}">'.format(self.customer_id)

class Booking(Model):
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self._client = client
        self.vehicle = Vehicle(client, **self.vehicule)
        self.expiration_date = parse_date(self.expiration_date)
        self.date = parse_date(self.date)
        del self.vehicule

    def __repr__(self):
        return '<Booking id="{}" vehicle_id="{}">'.format(self.id, self.vehicle.id)
