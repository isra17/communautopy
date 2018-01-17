import time
import requests
import json
import zeep
import os.path

from zeep.transports import Transport
from .models import Proposals, Login, Booking

WSDL_PATH = os.path.join(os.path.dirname(__file__), './LSIBookingService.wsdl')
LOGIN_URL = 'https://www.reservauto.net/Scripts/Client/Ajax/Mobile/Login.asp'
GET_STATIONPARKING_AVAILABILITY_URL = 'https://www.reservauto.net/WCF/Reservauto/StationParking/StationParkingService.svc/Get_StationParking_Availability'

class NotAuthenticatedError(Exception):
    pass

class Client:
    def __init__(self, session=None):
        self._session = session
        transport = Transport(session=session) if session else None
        self._api_client = zeep.Client(WSDL_PATH, transport=transport)

    def get_vehicle_proposals(self, latitude, longitude):
        response = self._api_client.service.GetVehicleProposals(Latitude=latitude, Longitude=longitude)
        proposals = self._parse_jsonp(response)
        return Proposals(self, **proposals)

    def auth(self, username, password, branch_id=1):
        query = {
            'BranchID': branch_id,
            'Password': password,
            'Username': username,
        }

        session = requests.Session()
        response = session.get(LOGIN_URL, params=query)
        response.raise_for_status()
        return Client(session)

    def login(self):
        if not self._session:
            raise NotAuthenticatedError()
        response = self._session.get(LOGIN_URL, params={'URLEnd': 'URLEnd'})
        response.raise_for_status()
        login = response.json()
        if not login['data'][0]['CustomerID']:
            raise NotAuthenticatedError()
        return [Login(self, **l) for l in login['data']]

    def get_current_booking(self, customer_id):
        booking = self._parse_jsonp(self._api_client.service.GetCurrentBooking(CustomerID=customer_id))
        return Booking(self, **booking) if booking else None

    def create_booking(self, customer_id, vehicle_id):
        return self._parse_jsonp(self._api_client.service.CreateBooking(CustomerID=customer_id, VehicleID=vehicle_id))

    def cancel_booking(self, customer_id, vehicle_id):
        return self._parse_jsonp(self._api_client.service.CancelBooking(CustomerID=customer_id, VehicleID=vehicle_id))

    @staticmethod
    def _parse_jsonp(jsonp):
        raw_json = jsonp[jsonp.index('(') + 1:jsonp.rindex(')')]
        return json.loads(raw_json)
