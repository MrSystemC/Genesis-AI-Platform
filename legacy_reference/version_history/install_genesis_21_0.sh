#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.1.0 AI Civilization Core ==="


mkdir -p ai_core
mkdir -p agents
mkdir -p memory
mkdir -p intelligence


touch ai_core/__init__.py
touch agents/__init__.py
touch memory/__init__.py
touch intelligence/__init__.py


echo "[1] Agent personality"


cat > agents/personality.py <<'PY'
import random


class Personality:


    def __init__(self):

        self.creativity=random.random()

        self.risk=random.random()

        self.logic=random.random()

        self.social=random.random()



    def profile(self):

        return {

        "creativity":round(self.creativity,2),

        "risk":round(self.risk,2),

        "logic":round(self.logic,2),

        "social":round(self.social,2)

        }
PY



echo "[2] Memory system"


cat > memory/memory.py <<'PY'
class Memory:


    def __init__(self):

        self.events=[]



    def remember(self,event):

        self.events.append(event)



    def recall(self):

        return self.events[-10:]
PY



echo "[3] Goals"


cat > agents/goals.py <<'PY'
class Goals:


    def __init__(self,role):

        self.role=role


    def current(self):

        goals={

        "entrepreneur":
        "create_company",

        "scientist":
        "discover",

        "engineer":
        "build",

        "leader":
        "expand"

        }


        return goals.get(

        self.role,

        "survive"

        )
PY



echo "[4] Decision engine"


cat > intelligence/decision.py <<'PY'
class DecisionEngine:


    def decide(
        self,
        agent,
        situation
    ):


        goal=agent.goal.current()



        if goal=="create_company":

            return "build_business"


        if goal=="discover":

            return "research"


        if goal=="build":

            return "create_technology"


        if goal=="expand":

            return "organize"


        return "work"
PY



echo "[5] Autonomous agent"


cat > ai_core/agent.py <<'PY'
from agents.personality import Personality
from agents.goals import Goals
from memory.memory import Memory
from intelligence.decision import DecisionEngine



class IntelligentAgent:


    def __init__(
        self,
        name,
        role
    ):

        self.name=name

        self.role=role

        self.energy=100

        self.knowledge=0

        self.personality=Personality()

        self.goal=Goals(role)

        self.memory=Memory()

        self.engine=DecisionEngine()



    def observe(self,world):

        self.memory.remember(

        {

        "population":
        len(world),

        "knowledge":
        self.knowledge

        }

        )



    def think(self,world):

        return self.engine.decide(

        self,

        world

        )



    def act(self,world):

        action=self.think(world)


        self.memory.remember(

        action

        )


        if action=="research":

            self.knowledge+=10


        if action=="create_technology":

            self.knowledge+=5


        self.energy-=1


        return action
PY



echo "[6] Civilization simulation"


cat > civilization_ai.py <<'PY'
from ai_core.agent import IntelligentAgent



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



world=agents



for day in range(20):


    print(
    "\nDAY",
    day
    )


    for agent in agents:


        agent.observe(world)


        action=agent.act(world)


        print(

        agent.name,

        agent.role,

        "->",

        action,

        "knowledge:",

        agent.knowledge

        )



print("\nAGENT PROFILES")


for agent in agents:


    print(

    agent.name,

    agent.personality.profile()

    )

PY



echo "Genesis-2.1.0 installed"

python civilization_ai.py


