import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


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
