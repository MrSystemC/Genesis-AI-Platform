from world import World
from population import create_population

from civilization_core import CivilizationCore
from city import City
from government_ai import GovernmentAI
from science import Science
from diplomacy_system import Diplomacy
from global_simulation import GlobalSimulation
from dashboard import display



world=World(
"Genesis Planet"
)



world.agents=create_population(
200
)



civilization=CivilizationCore(
"Genesis Civilization"
)



cities=[

City("Alpha City"),

City("Beta City"),

City("Gamma City")

]



for i,agent in enumerate(
    world.agents
):

    cities[
        i%3
    ].population.append(
        agent
    )



government=GovernmentAI()

science=Science()

diplomacy=Diplomacy()

events=GlobalSimulation()



for year in range(500):


    civilization.population=len(
        world.agents
    )


    civilization.advance()



    for city in cities:

        city.develop()



    science.research(
        civilization.knowledge
    )


    if year%50==0:


        event=events.event()


        civilization.record(
            event
        )


        decision=government.analyze(
            civilization
        )


        civilization.record(
            decision
        )



    if year%100==0:

        diplomacy.create(

        "Alpha City",

        "Beta City",

        "cooperation"

        )


    if year%25==0:

        display(

        civilization,

        cities,

        science

        )



print("\nHISTORY:")

for item in civilization.history:

    print(item)



print("\nDISCOVERIES:")

print(
science.discoveries
)


print("\nDIPLOMACY:")

print(
diplomacy.relations
)
