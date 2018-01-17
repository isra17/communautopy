import datetime
import sys
import getpass
import argparse
from haversine import haversine
from . import maps_service
from . import Client

client = Client()

def auth(username):
    password = getpass.getpass()
    return client.auth(username, password)

def cancel(args):
    auth_client = auth(args.username)
    login = auth_client.login()[0]
    if not login.cancel_booking():
        print('Failed to cancel booking')
        return 1
    print('Successfuly canceled booking')
    return 0

def current(args):
    auth_client = auth(args.username)
    login = auth_client.login()[0]
    current_booking = login.current_booking
    if current_booking:
        location = maps_service.Location.from_coord(current_booking.vehicle.position)
        time_left = current_booking.expiration_date - datetime.datetime.now()
        print('{} near "{}", expire at {}, {}m {}s left'.format(
            current_booking.vehicle, location, current_booking.expiration_date,
            time_left.seconds//60, time_left.seconds%60))
    else:
        print('No current booking')
        return 1
    return 0


def book(args):
    vehicle = None
    if args.near is None:
        location = maps_service.Location.locate()
    else:
        location = maps_service.Location.search(args.near)[0]
    print('Your location: {}'.format(location))
    proposals = client.get_vehicle_proposals(*location.position)
    print('{} vehicles available'.format(len(proposals.vehicles)))

    if args.id or args.no:
        try:
            if args.id:
                vehicle = next(v for v in proposals.vehicles if args.id == v.id )
            else:
                vehicle = next(v for v in proposals.vehicles if args.no == v.name )
        except StopIteration:
            print('Vehicle {} not available'.format(args.id or args.no))
            return 1

    else:
        vehicles = proposals.vehicles[:5]
        distances = maps_service.distances(proposals.user_position, [v.position for v in vehicles])
        cars = list(sorted(zip(vehicles, distances), key=lambda p: p[1]['duration']['value']))
        for i, (v, d) in enumerate(cars):
            print('[{}]: {} near "{}" at {} ({} walk)'.format(i, v.id, d['address'], d['distance']['text'], d['duration']['text']))
        car_n = int(input('Car choice: '))
        vehicle, _ = cars[car_n]

    auth_client = auth(args.username)
    login = auth_client.login()[0]
    if not login.book(vehicle):
        print('Failed to book vehicle')
        return 1

    print('Booking successful')
    return 0

parser = argparse.ArgumentParser()
parser.add_argument('--username', required=True, help='Account username')
subparsers = parser.add_subparsers()
book_parser = subparsers.add_parser('book', help='Book an automobile')
book_parser.add_argument("--near", nargs='?', help="Book a car close to the provided location")
book_parser.add_argument("--id", help="Book a car given its id")
book_parser.add_argument("--no", help="Book a car given 4 digits car number")
book_parser.set_defaults(func=book)
current_parser = subparsers.add_parser('current', help='Get current booking')
current_parser.set_defaults(func=current)
cancel_parser = subparsers.add_parser('cancel', help='Cancel current booking')
cancel_parser.set_defaults(func=cancel)
args = parser.parse_args()
if hasattr(args, 'func'):
    sys.exit(args.func(args))
else:
    parser.print_usage()
    sys.exit(1)
