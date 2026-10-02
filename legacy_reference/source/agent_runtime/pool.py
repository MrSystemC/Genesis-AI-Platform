from agent_runtime.agent import Agent

class AgentPool:

    def __init__(self):
        self.agents=[]

    def create(self,count):
        for i in range(count):
            self.agents.append(
            Agent(i)
            )

    def size(self):
        return len(self.agents)
