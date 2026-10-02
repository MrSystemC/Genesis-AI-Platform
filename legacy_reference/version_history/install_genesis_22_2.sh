#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-2.2.2 Multi-Civilization Evolution ==="


mkdir -p evolution
mkdir -p civilizations
mkdir -p migration
mkdir -p universe_history


touch evolution/__init__.py
touch civilizations/__init__.py
touch migration/__init__.py
touch universe_history/__init__.py



printf '%s\n' \
'class Civilization:' \
'' \
'    def __init__(self,name):' \
'        self.name=name' \
'        self.age=0' \
'        self.technology=1' \
'        self.population=1000' \
'        self.power=100' \
'' \
'    def evolve(self):' \
'        self.age+=1' \
'        self.population+=100' \
'        self.technology+=1' \
'        self.power+=10' \
> civilizations/civilization.py



printf '%s\n' \
'import random' \
'' \
'class PlanetGenerator:' \
'' \
'    def __init__(self):' \
'        self.planets=[]' \
'' \
'    def create(self,name):' \
'        planet={' \
'        "name":name,' \
'        "resources":random.randint(10000,100000)' \
'        }' \
'        self.planets.append(planet)' \
'        return planet' \
> evolution/planet_generator.py



printf '%s\n' \
'class Migration:' \
'' \
'    def __init__(self):' \
'        self.routes=[]' \
'' \
'    def move(self,civ,planet):' \
'        self.routes.append({' \
'        "civilization":civ.name,' \
'        "planet":planet["name"]' \
'        })' \
'' \
'    def status(self):' \
'        return self.routes' \
> migration/system.py



printf '%s\n' \
'class EvolutionEngine:' \
'' \
'    def __init__(self):' \
'        self.eras=[]' \
'' \
'    def update(self,civilization):' \
'        if civilization.technology >= 5:' \
'            self.eras.append("Space Age")' \
'        elif civilization.technology >= 3:' \
'            self.eras.append("Industrial Age")' \
'        else:' \
'            self.eras.append("Early Age")' \
'' \
'    def history(self):' \
'        return self.eras[-10:]' \
> evolution/engine.py



printf '%s\n' \
'class UniverseHistory:' \
'' \
'    def __init__(self):' \
'        self.events=[]' \
'' \
'    def record(self,event):' \
'        self.events.append(event)' \
'' \
'    def show(self):' \
'        return self.events[-10:]' \
> universe_history/history.py



printf '%s\n' \
'from evolution.planet_generator import PlanetGenerator' \
'from civilizations.civilization import Civilization' \
'from migration.system import Migration' \
'from evolution.engine import EvolutionEngine' \
'from universe_history.history import UniverseHistory' \
'' \
'generator=PlanetGenerator()' \
'migration=Migration()' \
'evolution=EvolutionEngine()' \
'history=UniverseHistory()' \
'' \
'earth=generator.create("Genesis Earth")' \
'mars=generator.create("Genesis Mars")' \
'alpha=generator.create("Alpha World")' \
'' \
'civilizations=[' \
'Civilization("Earth Civilization"),' \
'Civilization("Mars Civilization"),' \
'Civilization("Alpha Civilization")' \
']' \
'' \
'for year in range(20):' \
'' \
'    for civ in civilizations:' \
'        civ.evolve()' \
'        evolution.update(civ)' \
'' \
'    if year % 5 == 0:' \
'        migration.move(civilizations[0],mars)' \
'        history.record("New civilization era "+str(year))' \
'' \
'print("CIVILIZATIONS")' \
'for civ in civilizations:' \
'    print(civ.name,civ.population,civ.technology)' \
'' \
'print("MIGRATION")' \
'print(migration.status())' \
'' \
'print("EVOLUTION")' \
'print(evolution.history())' \
'' \
'print("HISTORY")' \
'print(history.show())' \
> evolution_test.py



echo "Checking syntax..."

python -m py_compile \
civilizations/civilization.py \
evolution/planet_generator.py \
migration/system.py \
evolution/engine.py \
universe_history/history.py \
evolution_test.py



echo "Running simulation..."

python evolution_test.py


echo "=== Genesis-2.2.2 COMPLETE ==="

