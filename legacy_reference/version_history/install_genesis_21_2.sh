#!/data/data/com.termux/files/usr/bin/bash

echo "=== Genesis-2.1.2 Autonomous AI Companies ==="


mkdir -p economy
mkdir -p companies
mkdir -p products


touch economy/__init__.py
touch companies/__init__.py
touch products/__init__.py


echo "[1] Product system"


cat > products/product.py <<'PY'
class Product:


    def __init__(
        self,
        name,
        creator
    ):

        self.name=name

        self.creator=creator

        self.sales=0

        self.price=100



    def sell(self):

        self.sales+=1


    def value(self):

        return self.sales*self.price
PY



echo "[2] Company system"


cat > companies/company.py <<'PY'
class AICompany:


    def __init__(
        self,
        name,
        founder
    ):

        self.name=name

        self.founder=founder

        self.employees=[]

        self.capital=1000

        self.revenue=0

        self.products=[]



    def hire(
        self,
        agent
    ):

        self.employees.append(
            agent
        )



    def create_product(
        self,
        product
    ):

        self.products.append(
            product
        )



    def operate(self):

        for product in self.products:

            product.sell()


        self.revenue += len(
            self.products
        )*100


        self.capital += self.revenue
PY



echo "[3] Investment system"


cat > economy/investment.py <<'PY'
class Investment:


    def invest(
        self,
        investor,
        company
    ):


        amount=500


        if investor.knowledge>0:


            company.capital+=amount


            return True


        return False
PY



echo "[4] Market system"


cat > economy/market.py <<'PY'
class Market:


    def __init__(self):

        self.companies=[]



    def register(
        self,
        company
    ):

        self.companies.append(
            company
        )



    def ranking(self):

        return sorted(

        self.companies,

        key=lambda x:x.revenue,

        reverse=True

        )
PY



echo "[5] Autonomous company simulation"


cat > company_simulation.py <<'PY'
from ai_core.agent import IntelligentAgent

from companies.company import AICompany

from products.product import Product

from economy.market import Market

from economy.investment import Investment



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
"investor"
)

]



market=Market()

investment=Investment()



company=AICompany(

"Genesis Future AI",

agents[0]

)



for agent in agents:

    company.hire(
        agent
    )



product=Product(

"AI Research Platform",

company.name

)



company.create_product(
product
)



market.register(
company
)



for year in range(20):


    print(
    "\nYEAR",
    year
    )


    company.operate()



    investment.invest(

    agents[1],

    company

    )


    print(

    "Capital:",
    company.capital

    )


    print(

    "Revenue:",
    company.revenue

    )


    print(

    "Sales:",
    product.sales

    )



print("\nMARKET RANKING")


for c in market.ranking():

    print(

    c.name,

    c.revenue

    )



