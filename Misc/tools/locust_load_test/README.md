# LocustIO Load Test
This is used to perform load testing on the applications within the overall system.

It tests the endpoints of the `UI-Server` and `Accessor` components of the HoloRepository system.

## Prerequisites
- LocustIO
- HoloRepository Azure FHIR Service Infra (EHR and HoloStorage)

## Testing
> Note: Testing is done with the assumption that the service contains data from the `holorepo_demo`. View `Misc/holorepo_demo` for more details.

To execute locust load test on the accessor or UI-Server.

First install LocustIO with `pipenv install --dev`

Then, depending on what you are testing, the following components must be running.
- Testing UI-Server: UI-Server and Accessor
- Testing Accessor: Accessor

Next, start the locust test service

```
locust -f <path_to_locustfile> --host=<component_host_url>
```

| Component | Locustfile             | Host                  |
|-----------|------------------------|-----------------------|
| UI-Server | locustfile-ui.py       | http://localhost:3001 |
| Accessor  | locustfile-accessor.py | http://localhost:3200 |

Finally, view the test interface via `http://127.0.0.1:8089/` and start the load test.

