import random
import numpy as np


class Resource:

    count = 0

    def __init__(self, name="Resource", init_price=10.0, mu_modifier=0.001, sigma_modifier=0.02):
        Resource.count += 1
        self.name = name
        self.id = Resource.count
        self.price = init_price
        # >>> mu
        # 0.0013410039457334778
        # >>> sigma
        # 0.03571855069950321
        self.mu = random.uniform(0, mu_modifier)  # Volatilité 0.001
        self.sigma = random.uniform(0, sigma_modifier)  # Hauteur du prix max 0.02
        self.sim_rets = np.random.normal(self.mu, self.sigma, 500)
        self.sim_prices = init_price * (self.sim_rets + 1).cumprod()

    def get_price(self, day):
        if day > len(self.sim_prices):
            raise RuntimeError('Simulation is too short')
        return self.sim_prices[day]

    def __repr__(self):
        return "{}[{}] ({}$)".format(self.name, self.id, self.price)


class Commodity(Resource):

    def __init__(self, recipe={}) -> None:
        pass
