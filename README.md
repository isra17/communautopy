Python API client for communauto's automobile services.

Command line api available to manage bookings:

## Book close to device location:
```
$ python -m communauto --username <USERNAME> book
```

## Book close to a location:
```
$ python -m communauto --username <USERNAME> book --near 'Bloc Shop Hochelaga'
```

## Book a car from its ID:
```
$ python -m communauto --username <USERNAME> book --id JTDKDTB31G112XXXX
```

## Book a car from its number:
```
$ python -m communauto --username <USERNAME> book --no 3001
```

## Get current booking:
```
$ python -m communauto --username <USERNAME> current
```

## Cancel current booking:
```
$ python -m communauto --username <USERNAME> cancel
```
