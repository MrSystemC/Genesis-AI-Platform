from runtime.agent_runtime import AgentRuntime
from runtime.simulation_cluster import SimulationCluster
from services30.simulation import SimulationService

from genesis_knowledge import genesis_knowledge
from genesis_governance import genesis_governance
from storage.database import storage


class GenesisCore:


    def __init__(self):

        self.cycle = 0

        self.world = {
            "name":"Genesis Prime",
            "age":0
        }

        self.agents = AgentRuntime()

        self.simulation = SimulationService()

        self.cluster = SimulationCluster()



    def boot(self):

        self.agents.spawn(1)

        self.cluster.run(
            self.world
        )




    def save_state(self):

        data = {
            "cycle": self.cycle,
            "world": self.world
        }

        storage.save({
            "state": data
        })



    def restore_state(self):

        data = storage.load()

        state=data.get("state")

        if state:

            self.cycle = state.get(
                "cycle",
                0
            )

            self.world = state.get(
                "world",
                self.world
            )



    def backup_state(self):

        storage.backup()


    def tick(self):

        self.cycle += 1


        self.world = self.simulation.tick(
            self.world
        )


        genesis_knowledge.tick()

        genesis_governance.tick()

        self.save_state()



    def status(self):

        return {

            "cycle":self.cycle,

            "world":self.world,

            "agents":
                self.agents.status(),

            "simulation":
                self.cluster.status(),

            "knowledge":
                genesis_knowledge.status_data(),

            "governance":
                genesis_governance.status()

        }



genesis_core = GenesisCore()
genesis_core.restore_state()
genesis_core.boot()
