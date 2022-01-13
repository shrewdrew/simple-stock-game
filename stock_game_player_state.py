class state:
    def __init__(self):
        # state0-wait to buy
        # state1-hold
        self.state=0
        self.score=1
        self.buy_price=0.

    def get_state(self):
        return(self.state)
    
    def get_buy_price(self):
        return(self.buy_price)

    def get_score(self):
        return(self.score)

    def buy(self, buy_price):
        assert self.state==0, ("buy when not waiting")
        self.buy_price=buy_price
        self.state=1

    def sell(self, sell_price):
        assert self.state==1, ("sell when not holding")
        self.score+=self.score*(sell_price-self.buy_price)
        self.state=0