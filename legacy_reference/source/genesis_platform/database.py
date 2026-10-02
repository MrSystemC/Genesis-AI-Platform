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
