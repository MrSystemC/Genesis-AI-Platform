#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.0.1 Platform Core ==="


mkdir -p genesis_platform
mkdir -p storage
mkdir -p users
mkdir -p worlds


cat > users/user.py <<'PY'
import uuid


class User:

    def __init__(self,username):

        self.id=str(uuid.uuid4())

        self.username=username

        self.plan="free"

        self.worlds=[]



    def add_world(self,world):

        self.worlds.append(world.id)
PY



cat > worlds/world.py <<'PY'
import uuid
import time


class DigitalWorld:


    def __init__(self,name,owner):

        self.id=str(uuid.uuid4())

        self.name=name

        self.owner=owner

        self.population=0

        self.age=0

        self.status="created"

        self.created=time.time()



    def start(self):

        self.status="running"



    def tick(self):

        if self.status=="running":

            self.age+=1

            self.population+=1
PY



cat > genesis_platform/database.py <<'PY'
import json
import os


class Storage:


    def __init__(self):

        self.file="storage/platform.json"

        if not os.path.exists(
            self.file
        ):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                    "users":[],
                    "worlds":[]
                    },
                    f
                )



    def load(self):

        with open(self.file) as f:

            return json.load(f)



    def save(self,data):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )
PY



cat > genesis_platform/platform.py <<'PY'
from genesis_platform.database import Storage


class GenesisPlatform:


    def __init__(self):

        self.storage=Storage()

        self.data=self.storage.load()



    def register_user(
        self,
        user
    ):

        self.data["users"].append(

        {
        "id":user.id,
        "name":user.username,
        "plan":user.plan
        }

        )

        self.storage.save(
            self.data
        )



    def register_world(
        self,
        world
    ):

        self.data["worlds"].append(

        {
        "id":world.id,
        "name":world.name,
        "owner":world.owner
        }

        )

        self.storage.save(
            self.data
        )



    def status(self):

        return {

        "users":
        len(self.data["users"]),

        "worlds":
        len(self.data["worlds"])

        }
PY



cat > genesis_platform/demo.py <<'PY'
from users.user import User
from worlds.world import DigitalWorld
from genesis_platform.platform import GenesisPlatform



platform=GenesisPlatform()



user=User(
"Founder"
)



world=DigitalWorld(
"Genesis Alpha",
user.username
)



user.add_world(
world
)



platform.register_user(
user
)



platform.register_world(
world
)



world.start()



for i in range(10):

    world.tick()



print(
"GENESIS PLATFORM ONLINE"
)


print(
platform.status()
)


print(
{
"name":world.name,
"age":world.age,
"population":world.population,
"status":world.status
}
)
PY



touch genesis_platform/__init__.py
touch users/__init__.py
touch worlds/__init__.py


echo "Genesis-2.0.1 installed"

python genesis_platform/demo.py

