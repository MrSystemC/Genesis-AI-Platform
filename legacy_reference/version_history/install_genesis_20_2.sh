#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.0.2 Web Control Panel ==="


echo "[1] Installing dependencies"

pip install fastapi uvicorn --quiet



mkdir -p web
mkdir -p api



echo "[2] Creating API server"


cat > api/server.py <<'PY'
from fastapi import FastAPI
from pydantic import BaseModel

import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from worlds.world import DigitalWorld


app=FastAPI(
    title="Genesis Platform API"
)


worlds=[]



class WorldCreate(BaseModel):

    name:str

    owner:str



@app.get("/")
def home():

    return {

    "system":
    "Genesis-2.0.2",

    "status":
    "online"

    }



@app.get("/worlds")
def get_worlds():

    return worlds



@app.post("/world/create")
def create_world(data:WorldCreate):


    world=DigitalWorld(

        data.name,

        data.owner

    )


    world.start()


    worlds.append(

    {

    "id":world.id,

    "name":world.name,

    "owner":world.owner,

    "status":world.status

    }

    )


    return worlds[-1]
PY



echo "[3] Creating dashboard"


cat > web/index.html <<'HTML'
<!DOCTYPE html>

<html>

<head>

<title>
Genesis Control Panel
</title>


<style>

body{

background:#111;

color:#0f0;

font-family:monospace;

padding:30px;

}


button{

padding:10px;

background:#0f0;

border:0;

}

</style>


</head>


<body>


<h1>
Genesis Civilization Control Panel
</h1>


<h3>
System Status
</h3>


<div id="status">
loading...
</div>


<button onclick="load()">
Refresh
</button>


<script>


async function load(){


let r=await fetch(
'http://127.0.0.1:8000/'
);


let d=await r.json();


document.getElementById(
"status"
).innerHTML=

JSON.stringify(
d
);


}


load();


</script>


</body>

</html>
HTML



echo "[4] Creating launcher"


cat > start_genesis_web.sh <<'SH'
#!/data/data/com.termux/files/usr/bin/bash

echo "Starting Genesis Web Panel..."

uvicorn api.server:app --host 0.0.0.0 --port 8000

SH


chmod +x start_genesis_web.sh


echo ""
echo "Genesis-2.0.2 installed"
echo ""
echo "START:"
echo "./start_genesis_web.sh"

