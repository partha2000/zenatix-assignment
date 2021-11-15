from tqdm import tqdm
from time import sleep
import psutil

process_id = 1
for process_id in psutil.pids()[-10:]:
    process = psutil.Process(process_id)
    print("PID #",process.name()," RAM = ",round(process.memory_percent(),2)," CPU = ",process.cpu_percent())

with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
    while True:
        rambar.n=psutil.virtual_memory().percent
        cpubar.n=psutil.cpu_percent()
        rambar.refresh()
        cpubar.refresh()
        sleep(0.5)