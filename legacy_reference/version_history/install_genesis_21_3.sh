#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.1.3 Autonomous Civilization Economy ==="


mkdir -p economy_engine
mkdir -p industries
mkdir -p trade


touch economy_engine/__init__.py
touch industries/__init__.py
touch trade/__init__.py



echo "[1] Labor Market"


cat > economy_engine/labor.py <<'PY'
class LaborMarket:


    def __init__(self):

        self.jobs=[]



    def register_job(
        self,
        company,
        role
    ):

        self.jobs.append(

        {
        "company":company.name,
        "role":role
        }

        )



    def status(self):

        return len(
            self.jobs
        )
PY



echo "[2] Industry system"


cat > industries/industry.py <<'PY'
class Industry:


    def __init__(self,name):

        self.name=name

        self.companies=[]

        self.production=0



    def add_company(self,company):

        self.companies.append(
            company
        )



    def produce(self):

        self.production += len(
            self.companies
        )*100
PY



echo "[3] Market prices"


cat > economy_engine/market.py <<'PY'
class Market:


    def __init__(self):

        self.products={}



    def add_product(
        self,
        name,
        price
    ):

        self.products[name]=price



    def change_prices(self):

        for product in self.products:

            self.products[product]+=10
PY



echo "[4] Trade system"


cat > trade/trade.py <<'PY'
class Trade:


    def __init__(self):

        self.transactions=[]



    def execute(
        self,
        seller,
        buyer,
        product
    ):

        self.transactions.append(

        {

        "seller":seller,

        "buyer":buyer,

        "product":product

        }

        )
PY



echo "[5] Economic crisis"


cat > economy_engine/crisis.py <<'PY'
import random


class Crisis:


    def check(
        self,
        companies
    ):


        affected=[]


        for company in companies:


            if random.random()<0.2:

                company.capital-=200


                affected.append(
                    company.name
                )


        return affected
PY



echo "[6] Civilization economy simulation"


cat > economy_simulation.py <<'PY'
from ai_core.agent import IntelligentAgent

from companies.company import AICompany

from products.product import Product

from industries.industry import Industry

from economy_engine.labor import LaborMarket

from economy_engine.market import Market

from economy_engine.crisis import Crisis

from trade.trade import Trade



agents=[]


for i in range(20):

    agents.append(

    IntelligentAgent(

    "Agent_"+str(i),

    "entrepreneur"

    )

    )



companies=[]


for i,agent in enumerate(agents):


    company=AICompany(

    "AI Company "+str(i),

    agent

    )


    product=Product(

    "Product_"+str(i),

    company.name

    )


    company.create_product(
        product
    )


    companies.append(
        company
    )



industry=Industry(
"Artificial Intelligence"
)


for company in companies:

    industry.add_company(
        company
    )



labor=LaborMarket()

market=Market()

crisis=Crisis()

trade=Trade()



for company in companies:

    labor.register_job(
        company,
        "AI Worker"
    )



market.add_product(
"AI Service",
100
)



for year in range(30):


    print(
    "\nYEAR",
    year
    )


    for company in companies:

        company.operate()



    industry.produce()



    market.change_prices()



    affected=crisis.check(
        companies
    )


    if affected:

        print(
        "CRISIS:",
        affected
        )



    print(

    "Companies:",
    len(companies)

    )


    print(

    "Production:",
    industry.production

    )


    print(

    "Jobs:",
    labor.status()

    )


print("\nMARKET")

print(
market.products
)


print("\nTRADE")

trade.execute(
"Company A",
"Company B",
"AI Service"
)


print(
trade.transactions
)

