from elasticsearch import Elasticsearch

time_range_begin = '12:00:00'
time_range_end = '13:00:00'

total_response_time = 0
es = Elasticsearch()
res = es.search(
    index="stoptimes",
    body={
        "query": {
            "bool": {
                "filter": [{
                    "range": {
                        "arrival_time": {
                            "gte": time_range_begin
                        }
                    }
                }, {
                    "range": {
                        "departure_time": {
                            "lte": time_range_end
                        }
                    }
                }]
            }
        }
    })
size = res.get('hits').get('total')
if size > 10:
    res = es.search(
        index="stoptimes",
        size=size,
        body={
            "query": {
                "bool": {
                    "filter": [{
                        "range": {
                            "arrival_time": {
                                "gte": time_range_begin
                            }
                        }
                    }, {
                        "range": {
                            "departure_time": {
                                "lte": time_range_end
                            }
                        }
                    }]
                }
            }
        })
response_time = res.get('took')
total_response_time += response_time
trip_id_list = res.get('hits').get('hits')
trip_id_set = set()
for trip_id in trip_id_list:
    trip_id_set.add(trip_id.get('_source').get('trip_id'))
bus_list = set()
for trip_id in trip_id_set:
    res = es.search(
        index="trips", body={"query": {
            "term": {
                "trip_id": trip_id
            }
        }})
    response_time = res.get('took')
    total_response_time += response_time
    bus_list.add(
        res.get('hits').get('hits')[0].get('_source').get('trip_headsign'))
print("List of all buses:")
for bus in bus_list:
    print(bus)
print("Response time:", total_response_time)
