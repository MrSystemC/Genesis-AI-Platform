class Investment:


    def invest(self,investor,company):

        amount=500


        if investor.knowledge>=0:

            company.capital+=amount

            return True


        return False
