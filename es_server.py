import logging
from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    if _es.ping():
        print('es server running')
    else:
        print('could not connect!')
    return _es

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "PID": {
                        "type": "integer"
                    },
                    "Name": {
                        "type": "text"
                    },
                    "RAM": {
                        "type": "integer"
                    },
                    "CPU": {
                        "type": "integer"
                    },
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        else:
            print("Index already created")
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='process_montior', body=record)
        print("added successfully!")
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def show_data(object,procmonindex,id):
    # try:
        res = object.get(index=procmonindex, doc_type="process_monitor", id=id)
        print(res["_source"])
    # except:
        # print("Not found")
    

if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)

