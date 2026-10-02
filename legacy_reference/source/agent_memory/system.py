class AgentMemory:

    def __init__(self):
        self.memory={}

    def save(self,agent,event):
        if agent.id not in self.memory:
            self.memory[agent.id]=[]

        self.memory[agent.id].append(event)

    def get(self,agent):
        return self.memory.get(agent.id,[])
