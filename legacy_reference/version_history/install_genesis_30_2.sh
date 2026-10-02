#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-3.0.2 Web Dashboard Interface ==="


mkdir -p dashboard30
mkdir -p web30


touch dashboard30/__init__.py
touch web30/__init__.py



echo "[1] Dashboard backend"


printf '%s\n' \
'class Dashboard:' \
'' \
'    def __init__(self):' \
'        self.title="Genesis Control Panel"' \
'' \
'    def status(self,data):' \
'        return {' \
'        "dashboard":self.title,' \
'        "data":data' \
'        }' \
> dashboard30/system.py



echo "[2] Web interface"



printf '%s\n' \
'from fastapi import FastAPI' \
'from fastapi.responses import HTMLResponse' \
'from pydantic import BaseModel' \
'' \
'from services30.users import UserService' \
'from services30.universe import UniverseService' \
'from dashboard30.system import Dashboard' \
'' \
'app=FastAPI(' \
'title="Genesis Dashboard"' \
')' \
'' \
'users=UserService()' \
'universes=UniverseService()' \
'dashboard=Dashboard()' \
'' \
'class WorldRequest(BaseModel):' \
'    name:str' \
'    owner:str' \
'' \
'@app.get("/",response_class=HTMLResponse)' \
'def home():' \
'    return """' \
'    <html>' \
'    <body>' \
'    <h1>Genesis Control Panel</h1>' \
'    <p>Artificial Universe Platform</p>' \
'    <a href="/status">System Status</a>' \
'    </body>' \
'    </html>' \
'    """' \
'' \
'@app.get("/status")' \
'def status():' \
'    return dashboard.status({' \
'    "users":len(users.users),' \
'    "universes":len(universes.universes)' \
'    })' \
'' \
'@app.post("/create_world")' \
'def create_world(data:WorldRequest):' \
'    return universes.create(' \
'    data.name,' \
'    data.owner' \
'    )' \
> web30/dashboard.py



echo "[3] Dashboard test"



printf '%s\n' \
'from dashboard30.system import Dashboard' \
'' \
'd=Dashboard()' \
'' \
'print(' \
'd.status({' \
'"users":1,' \
'"universes":3' \
'})' \
> dashboard_test30.py



echo "Checking syntax..."

python -m py_compile \
dashboard30/system.py \
web30/dashboard.py \
dashboard_test30.py



echo "Running dashboard test..."

python dashboard_test30.py


echo "=== Genesis-3.0.2 COMPLETE ==="

