import uuid
import random


companies=[]


def create_company(industry):

    company={
        "id":str(uuid.uuid4()),

        "name":
        "Genesis Digital Company",

        "industry":industry,

        "capital":
        random.randint(100000,10000000),

        "employees":
        random.randint(5,500),

        "technology_level":
        random.randint(1,100),

        "market_share":
        random.randint(1,50),

        "simulation":{

            "years":10,

            "growth":
            random.randint(50,1000),

            "revenue":
            random.randint(1000000,1000000000)
        }
    }


    companies.append(company)

    return company



def economy_simulation(industry):

    result=[]

    for i in range(10):

        result.append(
            create_company(industry)
        )


    result.sort(
        key=lambda x:x["simulation"]["revenue"],
        reverse=True
    )


    return {
        "market":industry,
        "companies":result,
        "winner":result[0]
    }



def status():

    return {
        "engine":"Digital Economy",
        "status":"online",
        "companies":len(companies)
    }
