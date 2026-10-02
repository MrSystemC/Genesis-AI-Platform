class Market:


    def __init__(self):

        self.companies=[]



    def register(self,company):

        self.companies.append(company)



    def ranking(self):

        return sorted(
            self.companies,
            key=lambda x:x.revenue,
            reverse=True
        )
