#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-3.0.4 Simulation Runtime Platform ==="


mkdir -p runtime30
mkdir -p queue30
mkdir -p clock30
mkdir -p monitor30


touch runtime30/__init__.py
touch queue30/__init__.py
touch clock30/__init__.py
touch monitor30/__init__.py



echo "[1] World clock"


printf '%s\n' \
'class WorldClock:' \
'' \
'    def __init__(self):' \
'        self.time=0' \
'' \
'    def tick(self):' \
'        self.time+=1' \
'        return self.time' \
> clock30/clock.py



echo "[2] Simulation queue"


printf '%s\n' \
'class SimulationQueue:' \
'' \
'    def __init__(self):' \
'        self.tasks=[]' \
'' \
'    def add(self,task):' \
'        self.tasks.append(task)' \
'' \
'    def next(self):' \
'        if self.tasks:' \
'            return self.tasks.pop(0)' \
'        return None' \
'' \
'    def size(self):' \
'        return len(self.tasks)' \
> queue30/system.py



echo "[3] Runtime worker"


printf '%s\n' \
'class SimulationWorker:' \
'' \
'    def __init__(self):' \
'        self.results=[]' \
'' \
'    def run(self,world):' \
'        world["age"]+=1' \
'        world["events"]+=1' \
'        self.results.append(world.copy())' \
'        return world' \
'' \
'    def history(self):' \
'        return self.results' \
> runtime30/worker.py



echo "[4] State monitor"


printf '%s\n' \
'class RuntimeMonitor:' \
'' \
'    def status(self,worlds):' \
'        return {' \
'        "worlds":len(worlds),' \
'        "active":True' \
'        }' \
> monitor30/system.py



echo "[5] Runtime simulation test"


printf '%s\n' \
'from clock30.clock import WorldClock' \
'from queue30.system import SimulationQueue' \
'from runtime30.worker import SimulationWorker' \
'from monitor30.system import RuntimeMonitor' \
'' \
'clock=WorldClock()' \
'queue=SimulationQueue()' \
'worker=SimulationWorker()' \
'monitor=RuntimeMonitor()' \
'' \
'worlds=[' \
'{"name":"Genesis Alpha","age":0,"events":0},' \
'{"name":"Genesis Beta","age":0,"events":0}' \
']' \
'' \
'for world in worlds:' \
'    queue.add(world)' \
'' \
'while queue.size()>0:' \
'    world=queue.next()' \
'    year=clock.tick()' \
'    worker.run(world)' \
'    print("YEAR",year,world)' \
'' \
'print("MONITOR")' \
'print(monitor.status(worlds))' \
'' \
'print("HISTORY")' \
'print(worker.history())' \
> runtime_test30.py



echo "Checking syntax..."

python -m py_compile \
clock30/clock.py \
queue30/system.py \
runtime30/worker.py \
monitor30/system.py \
runtime_test30.py



echo "Running simulation runtime..."

python runtime_test30.py


echo "=== Genesis-3.0.4 COMPLETE ==="

