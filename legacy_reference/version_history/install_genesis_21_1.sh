#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.1.1 Agent Society Network ==="


mkdir -p society
mkdir -p organizations
mkdir -p communication


touch society/__init__.py
touch organizations/__init__.py
touch communication/__init__.py


echo "[1] Communication system"


cat > communication/network.py <<'PY'
class CommunicationNetwork:


    def __init__(self):

        self.messages=[]



    def send(
        self,
        sender,
        receiver,
        message
    ):


        self.messages.append(

        {

        "from":sender.name,

        "to":receiver.name,

        "message":message

        }

        )



    def history(self):

        return self.messages[-10:]
PY



echo "[2] Reputation system"


cat > society/reputation.py <<'PY'
class Reputation:


    def __init__(self):

        self.scores={}



    def register(self,agent):

        self.scores[agent.name]=50



    def increase(self,agent,value):

        self.scores[agent.name]+=value



    def get(self,agent):

        return self.scores.get(
            agent.name,
            0
        )
PY



echo "[3] Relationship system"


cat > society/relationships.py <<'PY'
class Relationships:


    def __init__(self):

        self.links=[]



    def connect(
        self,
        a,
        b,
        relation
    ):

        self.links.append(

        {

        "agent1":a.name,

        "agent2":b.name,

        "type":relation

        }

        )
PY



echo "[4] Organization system"


cat > organizations/company.py <<'PY'
class Organization:


    def __init__(
        self,
        name,
        leader
    ):

        self.name=name

        self.leader=leader

        self.members=[]

        self.knowledge=0



    def add_member(
        self,
        agent
    ):

        self.members.append(
            agent
        )



    def develop(self):

        self.knowledge+=len(
            self.members
        )
PY



echo "[5] Leadership"


cat > society/leadership.py <<'PY'
class Leadership:


    def choose(
        self,
        agents
    ):


        return max(

        agents,

        key=lambda a:
        a.knowledge

        )
PY



echo "[6] Society simulation"


cat > society_simulation.py <<'PY'
from ai_core.agent import IntelligentAgent

from communication.network import CommunicationNetwork

from society.reputation import Reputation

from society.relationships import Relationships

from organizations.company import Organization

from society.leadership import Leadership



agents=[

IntelligentAgent(
"Alice",
"entrepreneur"
),

IntelligentAgent(
"Bob",
"scientist"
),

IntelligentAgent(
"John",
"engineer"
),

IntelligentAgent(
"Eve",
"leader"
)

]



network=CommunicationNetwork()

reputation=Reputation()

relations=Relationships()

leader=Leadership()



for agent in agents:

    reputation.register(agent)



company=Organization(

"Genesis AI Corporation",

agents[0]

)



for agent in agents:

    company.add_member(agent)



for day in range(20):


    print(
    "\nDAY",
    day
    )


    for agent in agents:


        action=agent.act(
            agents
        )


        print(

        agent.name,

        "->",

        action

        )


    network.send(

    agents[0],

    agents[1],

    "Need scientific research"

    )


    relations.connect(

    agents[0],

    agents[1],

    "cooperation"

    )


    reputation.increase(

    agents[0],

    1

    )


    company.develop()



chosen=leader.choose(
agents
)


print("\nORGANIZATION")

print(
company.name
)


print(
"Leader:",
chosen.name
)


print(
"Knowledge:",
company.knowledge
)


print("\nMESSAGES")

print(
network.history()
)


print("\nRELATIONS")

print(
relations.links
)


print("\nREPUTATION")

print(
reputation.scores
)

