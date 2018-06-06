from elasticsearch import Elasticsearch

name_stop = "barrington St [northbound] opposite Scotia Square"
total_response_time = 0

es = Elasticsearch()
res = es.search(
    index="stops", body={"query": {
        "term": {
            "name_stop": name_stop
        }
    }})
print(res)
size = res.get('hits').get('total')
if size > 10:
    res = es.search(
        index="stops",
        size=size,
        body={"query": {
            "term": {
                "name_stop": name_stop
            }
        }})
response_time0 = res.get('took')
total_response_time += response_time0
stop_id = res.get('hits').get('hits')[0].get('_source').get('stop_id')

res = es.search(
    index="stoptimes", body={"query": {
        "term": {
            "stop_id": stop_id
        }
    }})
size = res.get('hits').get('total')
if size > 10:
    res = es.search(
        index="stoptimes",
        size=size,
        body={"query": {
            "term": {
                "stop_id": stop_id
            }
        }})
response_time1 = res.get('took')
total_response_time += response_time1
list_stoptimes = res.get('hits').get('hits')
set_trip_id = set()
for stoptime in list_stoptimes:
    set_trip_id.add(stoptime.get('_source').get('trip_id'))

set_trip_headsign = set()
for trip_id in set_trip_id:
    res = es.search(
        index="trips", body={"query": {
            "term": {
                "trip_id": trip_id
            }
        }})
    size = res.get('hits').get('total')
    if size > 10:
        res = es.search(
            index="trips",
            size=size,
            body={"query": {
                "term": {
                    "trip_id": trip_id
                }
            }})
    response_time_cur = res.get('took')
    total_response_time += response_time_cur
    list_trips = res.get('hits').get('hits')
    for trip in list_trips:
        set_trip_headsign.add(trip.get('_source').get('trip_headsign'))
print("List of all buses:")
for bus in set_trip_headsign:
    print(bus)
print()
print("Total response time is:", total_response_time, "milliseconds")
