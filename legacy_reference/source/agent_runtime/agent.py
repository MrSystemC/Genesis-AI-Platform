class Agent:

    def __init__(self,id):
        self.id=id
        self.energy=100
        self.knowledge=0
        self.status="active"

    def act(self):
        self.energy-=1
        self.knowledge+=1

    def state(self):
        return {
        "id":self.id,
        "energy":self.energy,
        "knowledge":self.knowledge
        }
