#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-2.2.3 Universal Civilization Economy ==="


mkdir -p universal_economy
mkdir -p corporations
mkdir -p currency
mkdir -p trade_routes


touch universal_economy/__init__.py
touch corporations/__init__.py
touch currency/__init__.py
touch trade_routes/__init__.py



printf '%s\n' \
'class UniversalCurrency:' \
'' \
'    def __init__(self):' \
'        self.name="Genesis Credit"' \
'        self.supply=1000000' \
'' \
'    def issue(self,amount):' \
'        self.supply+=amount' \
'' \
'    def status(self):' \
'        return {' \
'        "currency":self.name,' \
'        "supply":self.supply' \
'        }' \
> currency/system.py



printf '%s\n' \
'class PlanetEconomy:' \
'' \
'    def __init__(self,name):' \
'        self.name=name' \
'        self.resources=100000' \
'        self.wealth=0' \
'' \
'    def produce(self):' \
'        self.resources-=1000' \
'        self.wealth+=5000' \
'' \
'    def status(self):' \
'        return {' \
'        "planet":self.name,' \
'        "resources":self.resources,' \
'        "wealth":self.wealth' \
'        }' \
> universal_economy/planet_economy.py



printf '%s\n' \
'class SpaceCorporation:' \
'' \
'    def __init__(self,name):' \
'        self.name=name' \
'        self.capital=10000' \
'        self.trade_volume=0' \
'' \
'    def trade(self):' \
'        self.trade_volume+=1000' \
'        self.capital+=2000' \
'' \
'    def status(self):' \
'        return {' \
'        "company":self.name,' \
'        "capital":self.capital,' \
'        "trade":self.trade_volume' \
'        }' \
> corporations/company.py



printf '%s\n' \
'class TradeNetwork:' \
'' \
'    def __init__(self):' \
'        self.routes=[]' \
'' \
'    def create(self,origin,destination,resource):' \
'        self.routes.append({' \
'        "from":origin,' \
'        "to":destination,' \
'        "resource":resource' \
'        })' \
'' \
'    def status(self):' \
'        return self.routes' \
> trade_routes/network.py



printf '%s\n' \
'from currency.system import UniversalCurrency' \
'from universal_economy.planet_economy import PlanetEconomy' \
'from corporations.company import SpaceCorporation' \
'from trade_routes.network import TradeNetwork' \
'' \
'currency=UniversalCurrency()' \
'' \
'earth=PlanetEconomy("Genesis Earth")' \
'mars=PlanetEconomy("Genesis Mars")' \
'alpha=PlanetEconomy("Alpha World")' \
'' \
'corp1=SpaceCorporation("Genesis Galactic Corp")' \
'corp2=SpaceCorporation("Nova Resources")' \
'' \
'network=TradeNetwork()' \
'' \
'network.create("Earth","Mars","Energy")' \
'network.create("Mars","Alpha","Minerals")' \
'' \
'planets=[earth,mars,alpha]' \
'companies=[corp1,corp2]' \
'' \
'for year in range(20):' \
'' \
'    for planet in planets:' \
'        planet.produce()' \
'' \
'    for company in companies:' \
'        company.trade()' \
'' \
'    currency.issue(10000)' \
'' \
'print("CURRENCY")' \
'print(currency.status())' \
'' \
'print("PLANETS")' \
'for planet in planets:' \
'    print(planet.status())' \
'' \
'print("CORPORATIONS")' \
'for company in companies:' \
'    print(company.status())' \
'' \
'print("TRADE ROUTES")' \
'print(network.status())' \
> economy_test.py



echo "Checking syntax..."

python -m py_compile \
currency/system.py \
universal_economy/planet_economy.py \
corporations/company.py \
trade_routes/network.py \
economy_test.py



echo "Running universal economy simulation..."

python economy_test.py


echo "=== Genesis-2.2.3 COMPLETE ==="

