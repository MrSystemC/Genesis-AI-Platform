#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-3.0.1 Real Web API Platform ==="


echo "[1] Installing FastAPI"

pip install fastapi uvicorn --quiet



mkdir -p api30
mkdir -p services30


touch api30/__init__.py
touch services30/__init__.py



echo "[2] User service"


printf '%s\n' \
'class UserService:' \
'' \
'    def __init__(self):' \
'        self.users=[]' \
'' \
'    def create(self,name):' \
'        user={' \
'        "name":name' \
'        }' \
'        self.users.append(user)' \
'        return user' \
'' \
'    def list(self):' \
'        return self.users' \
> services30/users.py



echo "[3] Universe service"


printf '%s\n' \
'class UniverseService:' \
'' \
'    def __init__(self):' \
'        self.universes=[]' \
'' \
'    def create(self,name,owner):' \
'        universe={' \
'        "name":name,' \
'        "owner":owner,' \
'        "status":"running",' \
'        "age":0' \
'        }' \
'        self.universes.append(universe)' \
'        return universe' \
'' \
'    def list(self):' \
'        return self.universes' \
> services30/universe.py



echo "[4] Simulation service"


printf '%s\n' \
'class SimulationService:' \
'' \
'    def tick(self,universe):' \
'        universe["age"]+=1' \
'        return universe' \
> services30/simulation.py



echo "[5] API server"


printf '%s\n' \
'from fastapi import FastAPI' \
'from pydantic import BaseModel' \
'' \
'from services30.users import UserService' \
'from services30.universe import UniverseService' \
'from services30.simulation import SimulationService' \
'' \
'app=FastAPI(' \
'title="Genesis 3 Platform"' \
')' \
'' \
'users=UserService()' \
'universes=UniverseService()' \
'simulation=SimulationService()' \
'' \
'class UserRequest(BaseModel):' \
'    name:str' \
'' \
'class UniverseRequest(BaseModel):' \
'    name:str' \
'    owner:str' \
'' \
'@app.get("/")' \
'def home():' \
'    return {' \
'    "system":"Genesis-3.0.1",' \
'    "status":"online"' \
'    }' \
'' \
'@app.post("/users")' \
'def create_user(data:UserRequest):' \
'    return users.create(data.name)' \
'' \
'@app.get("/users")' \
'def get_users():' \
'    return users.list()' \
'' \
'@app.post("/universes")' \
'def create_universe(data:UniverseRequest):' \
'    return universes.create(data.name,data.owner)' \
'' \
'@app.get("/universes")' \
'def get_universes():' \
'    return universes.list()' \
> api30/server.py



echo "[6] API test"


printf '%s\n' \
'from services30.users import UserService' \
'from services30.universe import UniverseService' \
'from services30.simulation import SimulationService' \
'' \
'users=UserService()' \
'universes=UniverseService()' \
'sim=SimulationService()' \
'' \
'user=users.create("Founder")' \
'' \
'world=universes.create(' \
'"Genesis World",' \
'user["name"]' \
')' \
'' \
'sim.tick(world)' \
'' \
'print("USER")' \
'print(user)' \
'' \
'print("WORLD")' \
'print(world)' \
'' \
'print("API READY")' \
> api_test30.py



echo "Checking syntax..."

python -m py_compile \
services30/users.py \
services30/universe.py \
services30/simulation.py \
api30/server.py \
api_test30.py



echo "Running API core test..."

python api_test30.py


echo "=== Genesis-3.0.1 COMPLETE ==="

