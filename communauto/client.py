import json
import zeep
import os.path

from .models import Proposals

WSDL_PATH = os.path.join(os.path.dirname(__file__), './LSIBookingService.wsdl')

class Client:
    def __init__(self):
        self._api_client = zeep.Client(WSDL_PATH)

    def get_vehicle_proposals(self, latitude, longitude):
        response = self._api_client.service.GetVehicleProposals(Latitude=latitude, Longitude=longitude)
        proposals = self._parse_jsonp(response)
        return Proposals(self._api_client, **proposals)

    @staticmethod
    def _parse_jsonp(jsonp):
        raw_json = jsonp[jsonp.index('(') + 1:jsonp.rindex(')')]
        return json.loads(raw_json)
