import matplotlib.pyplot as plt
from models.resource import Resource
from models.agent import Baker
from constants.const import *

def plot_prices():
    for _ in range(100):
        r = Resource(init_price=1.2)
        plt.axhline(1.2)
        plt.plot(r.sim_prices)
    plt.show()

def basic_loop(baker, wheat_kg, wheat_t, water):
    prices = []
    for i in range(3):
        wheat_kg_price = wheat_kg.get_price(i)
        wheat_t_price = wheat_t.get_price(i)
        water_price = water.get_price(i)
        if baker.can_or_should_buy_wheat(wheat_kg_price, wheat_t_price):
            baker.buy_wheat()
        if baker.can_or_should_buy_water(water_price):
            baker.buy_water(water_price)
        baker.produce_flour()
        baker.produce_bread()
        prices.append(baker.price_limit)
        baker.sell_bread()
        print(baker)
    plt.plot(baker.bread_stock)
    plt.plot(baker.money)
    plt.show()
    plt.plot(prices)
    plt.show()
    plt.plot(wheat_t.sim_prices)
    plt.plot(wheat_kg.sim_prices)
    plt.plot(water.sim_prices)
    plt.show()

def main():
    wheat_kg = Resource(name='Wheat(KG)', init_price=WHEAT_KG_PRICE) # grams
    wheat_t = Resource(name='Wheat(T)', init_price=WHEAT_T_PRICE)  # grams
    water = Resource(name='Water', init_price=WATER_PRICE) # Liter
    baker = Baker(money=1000)
    print(baker)
    buying_unit, quantity = baker.can_or_should_buy_wheat(wheat_kg.sim_prices[0], wheat_t.sim_prices[0])
    wheat_price = wheat_t.sim_prices[0] if buying_unit == 't' else wheat_kg.sim_prices[0]
    baker.buy_wheat(wheat_price, buying_unit, quantity)
    print(baker.checking_account)
    # Water
    buying_unit, quantity = baker.can_or_should_buy_water(water.sim_prices[0])
    baker.buy_water(water.sim_prices[0], buying_unit, quantity)
    print(baker)
    print(baker.checking_account)
    # Produce flour
    baker.produce_flour()
    # Produce Bread
    bread_amount = baker.bread_stock.balance
    print(baker)
    baker.produce_bread()
    print('Produced {} bread'.format(baker.bread_stock.balance - bread_amount))
    print('Baker could get {}'.format(baker.bread_stock.balance*baker.price_limit))
    print(baker)
if __name__ == '__main__':
    main()