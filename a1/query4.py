from elasticsearch import Elasticsearch

es = Elasticsearch()
total_response_time = 0

res = es.search(index="stoptimes", size=3, body={"aggs": {
            "stop_id": {
                "terms": {"field": "stop_id"}
                }
            }})
response_time = res.get('took')
buckets = res.get('aggregations').get('stop_id').get('buckets')
print("The top 3 busiest bus stops are:")
for i in range(3):
    print("Stop ID", buckets[i].get('key'))
