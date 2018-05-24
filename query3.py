from elasticsearch import Elasticsearch

trip_headsign = "330 HALIFAX"
route_id = "330-121"
total_response_time = 0

es = Elasticsearch()
res = es.search(index="trips", body={
    "query": {
        "bool": {
            "filter": [
                {"term": {"trip_headsign": trip_headsign}},
                {"term": {"route_id": route_id}}
            ]
        }
    }
})
size = res.get('hits').get('total')
if size > 10:
    res = es.search(
        index="trips",
        size=size,
        body={
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"trip_headsign": trip_headsign}},
                        {"term": {"route_id": route_id}}
                    ]
                }
            }
        }
    )
total_response_time += res.get('took')
trip_id_list = res.get('hits').get('hits')
trip_id_set = set()
for trip_id in trip_id_list:
    trip_id_set.add(trip_id.get('_source').get('trip_id'))
print("List of route (trip_id):")
for trip_id in trip_id_set:
    print(trip_id)
print("Reponse time:", total_response_time)