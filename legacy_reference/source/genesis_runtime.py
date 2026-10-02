from services30.users import UserService
from services30.universe import UniverseService
from services30.simulation import SimulationService
from universes3.universe import Universe
from agents.agent_model import AIAgent
from companies.company import AICompany
from economy.market import Market
from products.product import Product


class GenesisRuntime:

    def __init__(self):

        self.users = UserService()
        self.universes = UniverseService()
        self.simulation = SimulationService()
        self.market = Market()

        self.worlds = []
        self.agents = []
        self.companies = []


    def boot(self):

        user = self.users.create("Founder")

        world = Universe(
            "Genesis Prime",
            "Founder"
        )

        self.universes.create(
            "Genesis Prime",
            "Founder"
        )

        world.start()


        agent = AIAgent(
            "Genesis Builder",
            "engineer",
            [
                "software",
                "research",
                "innovation"
            ]
        )


        company = AICompany(
            "Genesis Technologies",
            agent
        )

        company.hire(agent)


        product = Product(
            "Genesis AI Platform",
            agent
        )

        company.create_product(product)


        self.market.register(company)


        self.worlds.append(world)
        self.agents.append(agent)
        self.companies.append(company)


    def tick(self):

        for world in self.worlds:
            world.tick()

        for company in self.companies:
            company.operate()


    def status(self):

        return {
            "worlds": [
                {
                    "name": w.name,
                    "age": w.age,
                    "status": w.status
                }
                for w in self.worlds
            ],

            "agents": len(self.agents),

            "companies": [
                {
                    "name": c.name,
                    "capital": c.capital,
                    "revenue": c.revenue,
                    "products": len(c.products)
                }
                for c in self.companies
            ],

            "market": len(self.market.companies)
        }


genesis = GenesisRuntime()
genesis.boot()
