#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-2.2.1 Interplanetary Network ==="


mkdir -p interplanetary
mkdir -p resources
mkdir -p diplomacy

touch interplanetary/__init__.py
touch resources/__init__.py
touch diplomacy/__init__.py


printf '%s\n' \
'class SpaceTrade:' \
'' \
'    def __init__(self):' \
'        self.routes=[]' \
'' \
'    def create_route(self,a,b,resource):' \
'        self.routes.append({' \
'        "from":a,' \
'        "to":b,' \
'        "resource":resource' \
'        })' \
'' \
'    def status(self):' \
'        return self.routes' \
> interplanetary/trade.py



printf '%s\n' \
'class ResourceSystem:' \
'' \
'    def __init__(self):' \
'        self.resources={}' \
'' \
'    def add(self,planet,name,value):' \
'        self.resources[planet]={name:value}' \
'' \
'    def get(self):' \
'        return self.resources' \
> resources/system.py



printf '%s\n' \
'class Diplomacy:' \
'' \
'    def __init__(self):' \
'        self.treaties=[]' \
'' \
'    def create(self,a,b,status):' \
'        self.treaties.append({' \
'        "a":a,' \
'        "b":b,' \
'        "status":status' \
'        })' \
'' \
'    def list(self):' \
'        return self.treaties' \
> diplomacy/system.py



printf '%s\n' \
'from interplanetary.trade import SpaceTrade' \
'from resources.system import ResourceSystem' \
'from diplomacy.system import Diplomacy' \
'' \
'trade=SpaceTrade()' \
'resources=ResourceSystem()' \
'diplomacy=Diplomacy()' \
'' \
'resources.add("Earth","energy",100000)' \
'resources.add("Mars","minerals",90000)' \
'' \
'trade.create_route("Earth","Mars","energy")' \
'trade.create_route("Mars","Earth","minerals")' \
'' \
'diplomacy.create("Earth","Mars","alliance")' \
'' \
'print("TRADE")' \
'print(trade.status())' \
'' \
'print("RESOURCES")' \
'print(resources.get())' \
'' \
'print("DIPLOMACY")' \
'print(diplomacy.list())' \
> interplanetary_test.py



echo "Checking files..."

python -m py_compile \
interplanetary/trade.py \
resources/system.py \
diplomacy/system.py \
interplanetary_test.py


echo "Running test..."

python interplanetary_test.py


echo "=== Genesis-2.2.1 COMPLETE ==="

