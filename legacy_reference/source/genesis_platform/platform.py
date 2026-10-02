from genesis_platform.database import Storage


class GenesisPlatform:


    def __init__(self):

        self.storage=Storage()

        self.data=self.storage.load()



    def register_user(self,user):

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



    def register_world(self,world):

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

        "users":len(self.data["users"]),

        "worlds":len(self.data["worlds"])

        }
