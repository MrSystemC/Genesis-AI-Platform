#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-2.4.1 Distributed Universe Computing ==="


mkdir -p distributed
mkdir -p nodes
mkdir -p queue
mkdir -p monitoring


touch distributed/__init__.py
touch nodes/__init__.py
touch queue/__init__.py
touch monitoring/__init__.py



echo "[1] Compute nodes"



printf '%s\n' \
'class ComputeNode:' \
'' \
'    def __init__(self,name,capacity):' \
'        self.name=name' \
'        self.capacity=capacity' \
'        self.load=0' \
'' \
'    def execute(self,task):' \
'        self.load+=task["size"]' \
'        return {' \
'        "node":self.name,' \
'        "task":task["name"]' \
'        }' \
'' \
'    def status(self):' \
'        return {' \
'        "name":self.name,' \
'        "load":self.load,' \
'        "capacity":self.capacity' \
'        }' \
> nodes/node.py



echo "[2] Task queue"



printf '%s\n' \
'class TaskQueue:' \
'' \
'    def __init__(self):' \
'        self.tasks=[]' \
'' \
'    def add(self,task):' \
'        self.tasks.append(task)' \
'' \
'    def get(self):' \
'        if self.tasks:' \
'            return self.tasks.pop(0)' \
'        return None' \
'' \
'    def size(self):' \
'        return len(self.tasks)' \
> queue/tasks.py



echo "[3] Load balancer"



printf '%s\n' \
'class LoadBalancer:' \
'' \
'    def choose(self,nodes):' \
'        return min(' \
'        nodes,' \
'        key=lambda x:x.load' \
'        )' \
> distributed/balancer.py



echo "[4] Simulation manager"



printf '%s\n' \
'class SimulationManager:' \
'' \
'    def __init__(self):' \
'        self.running=[]' \
'' \
'    def start(self,task,node):' \
'        result=node.execute(task)' \
'        self.running.append(result)' \
'        return result' \
'' \
'    def status(self):' \
'        return self.running' \
> distributed/simulation.py



echo "[5] Monitoring"



printf '%s\n' \
'class Monitor:' \
'' \
'    def report(self,nodes):' \
'        return [' \
'        node.status()' \
'        for node in nodes' \
'        ]' \
> monitoring/system.py



echo "[6] Distributed test"



printf '%s\n' \
'from nodes.node import ComputeNode' \
'from queue.tasks import TaskQueue' \
'from distributed.balancer import LoadBalancer' \
'from distributed.simulation import SimulationManager' \
'from monitoring.system import Monitor' \
'' \
'nodes=[' \
'ComputeNode("Node-A",1000),' \
'ComputeNode("Node-B",1000),' \
'ComputeNode("Node-C",1000)' \
']' \
'' \
'queue=TaskQueue()' \
'balancer=LoadBalancer()' \
'simulation=SimulationManager()' \
'monitor=Monitor()' \
'' \
'queue.add({"name":"Universe Alpha","size":100})' \
'queue.add({"name":"Universe Beta","size":200})' \
'queue.add({"name":"Universe Gamma","size":300})' \
'' \
'while queue.size()>0:' \
'    task=queue.get()' \
'    node=balancer.choose(nodes)' \
'    print(simulation.start(task,node))' \
'' \
'print("NODES")' \
'print(monitor.report(nodes))' \
'' \
'print("SIMULATIONS")' \
'print(simulation.status())' \
> distributed_test.py



echo "Checking syntax..."

python -m py_compile \
nodes/node.py \
queue/tasks.py \
distributed/balancer.py \
distributed/simulation.py \
monitoring/system.py \
distributed_test.py



echo "Running distributed computing test..."

python distributed_test.py


echo "=== Genesis-2.4.1 COMPLETE ==="

