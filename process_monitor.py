from tqdm import tqdm
from time import sleep
import psutil
from es_server import *

esObject = connect_elasticsearch()
# indexCreated = create_index(esObject,'procmon')

for process_id in psutil.pids():
    process = psutil.Process(process_id)
    print("PID #",process.pid,"PID name: ",process.name()," RAM = ",round(process.memory_percent(),2)," CPU = ",process.cpu_percent())
    doc = {"PID": process.pid, "Name": process.name(), "RAM":round(process.memory_percent(),2), "CPU":process.cpu_percent()}
    store_record(esObject, 'procmon', doc)
    

with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
    while True:
        rambar.n=psutil.virtual_memory().percent
        cpubar.n=psutil.cpu_percent()
        rambar.refresh()
        cpubar.refresh()
        sleep(0.5)


#### Database schema
# "PID": {
#         "type": "integer"
#     },
#     "Name": {
#         "type": "text"
#     },
#     "RAM": {
#         "type": "integer"
#     },
#     "CPU": {
#         "type": "integer"
#     },