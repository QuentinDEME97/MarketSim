from random import random, gauss
from constants.const import *
import math
import logging
import uuid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BankAcount:

    def __init__(self, holder=None, balance=0):
        if holder is None:
            raise RuntimeWarning('BankAccount should have a holder')
        self.holder = holder
        self.balance = balance
        self.transactions = []
        self.id = uuid.uuid4()

    def income(self, period, amount):
        if period is None or amount is None:
            raise RuntimeError('Period and amound should not be None')
        self.balance += amount
        self.transactions.append((period, amount))
    
    def pay(self, period, amount):
        if period is None or amount is None:
            raise RuntimeError('Period and amound should not be None')
        self.balance -= amount
        self.transactions.append((period, amount))

    def __repr__(self):
        return '{} balance: {}$ number_of_transactions: {}'.format(self.id, self.balance, len(self.transactions))

class Agent(object):
    """docstring for Agent."""

    def __init__(
        self,
        type="Abstract",
        interaction_mode=None,
        price_limit=None,
        initial_price=None,  # For setting market expectations,
        id='',
        money=0,
    ):
        super().__init__()
        self.id = id
        self.type = type
        self.money = money
        if interaction_mode == None:
            raise Warning("Agent needs interaction_mode")
        self.interaction_mode = interaction_mode
        self.age_day = 0

        if price_limit == None:
            raise Warning("Everyone has a price!")
        self.price_limit = price_limit

        # determine initial goal price
        if initial_price == None:
            initial_price = self.price_limit
        else:
            if self.type == "buyer":
                initial_price = min(initial_price, self.price_limit)
            elif self.type == "seller":
                initial_price = max(initial_price, self.price_limit)

        self.goal_prices = [initial_price]  # initial value
        self.meetings = []

    def increase_age(self):
        self.age_day += 1

    def adjust_price(self, success=None, set_price=None, edit_last=False):
        if edit_last == False:
            if set_price != None:
                if (
                    self.type == "buyer"
                ):  # and self.interaction_mode != 'seller_asks_buyer_decides':
                    self.goal_prices.append(min(set_price, self.price_limit))
                if self.type == "seller":
                    self.goal_prices.append(max(set_price, self.price_limit))
            else:
                if success == None:
                    raise Warning("Need to know outcome to adjust price")
                if PRICE_ADJUST_MODE == "gauss":
                    # 1, with just a touch of variability to avoid weird states
                    adjust_amount = gauss(PRICE_ADJUST_MEAN, PRICE_ADJUST_DEV)
                if PRICE_ADJUST_MODE == "chance":
                    if random() < PRICE_ADJUST_CHANCE:
                        adjust_amount = PRICE_ADJUST_MEAN
                    else:
                        adjust_amount = 0
                if success == True:
                    if (
                        self.type == "buyer"
                    ):  # and self.interaction_mode != 'seller_asks_buyer_decides':
                        self.goal_prices.append(self.goal_prices[-1] - adjust_amount)
                    if self.type == "seller":
                        self.goal_prices.append(self.goal_prices[-1] + adjust_amount)
                if success == False:
                    if (
                        self.type == "buyer"
                    ):  # and self.interaction_mode != 'seller_asks_buyer_decides':
                        self.goal_prices.append(
                            min(self.goal_prices[-1] + adjust_amount, self.price_limit)
                        )
                    if self.type == "seller":
                        self.goal_prices.append(
                            max(self.goal_prices[-1] - adjust_amount, self.price_limit)
                        )
        else:
            if set_price != None:
                if (
                    self.type == "buyer"
                ):  # and self.interaction_mode != 'seller_asks_buyer_decides':
                    self.goal_prices[-1] = min(set_price, self.price_limit)
                if self.type == "seller":
                    self.goal_prices[-1] = max(set_price, self.price_limit)
            else:
                raise Warning(
                    "Hmm. I don't think it makes sense to edit the "
                    + "last goal price based on success or failure"
                )
    
    def __repr__(self):
        return 'Agent ' + self.id


class Buyer(Agent):

    nb_buyer = 0

    def __init__(
        self, interaction_mode=None, price_limit=None, initial_price=None, money=0
    ):
        Buyer.nb_buyer += 1
        self.id = "B" + str(Buyer.nb_buyer)
        super().__init__(
            type="buyer",
            interaction_mode=interaction_mode,
            price_limit=price_limit,
            initial_price=initial_price,  # Minimum price he can accept
            money=money,
            id = self.id
        )
        self.type = "buyer"
        self.money = money
        if interaction_mode == None:
            raise Warning("Agent needs interaction_mode")
        self.interaction_mode = interaction_mode

        if price_limit == None:
            raise Warning("Everyone has a price!")
        self.price_limit = price_limit

        # determine initial goal price
        if initial_price == None:
            initial_price = self.price_limit
        initial_price = min(initial_price, self.price_limit)

        self.goal_prices = [initial_price]  # initial value
        self.meetings = []

    def adjust_price(self, success=None, set_price=None, edit_last=False):
        if edit_last == False:
            if set_price != None:
                self.goal_prices.append(min(set_price, self.price_limit))
            else:
                if success == None:
                    raise Warning("Need to know outcome to adjust price")
                if PRICE_ADJUST_MODE == "gauss":
                    # 1, with just a touch of variability to avoid weird states
                    adjust_amount = gauss(PRICE_ADJUST_MEAN, PRICE_ADJUST_DEV)
                if PRICE_ADJUST_MODE == "chance":
                    if random() < PRICE_ADJUST_CHANCE:
                        adjust_amount = PRICE_ADJUST_MEAN
                    else:
                        adjust_amount = 0
                if success == True:
                    self.goal_prices.append(self.goal_prices[-1] - adjust_amount)
                if success == False:
                    self.goal_prices.append(
                        min(self.goal_prices[-1] + adjust_amount, self.price_limit)
                    )
        else:
            if set_price != None:
                self.goal_prices[-1] = min(set_price, self.price_limit)
            else:
                raise Warning(
                    "Hmm. I don't think it makes sense to edit the "
                    + "last goal price based on success or failure"
                )


class Seller(Agent):

    nb_seller = 0

    def __init__(
        self, interaction_mode=None, price_limit=None, initial_price=None, money=0
    ):
        Seller.nb_seller += 1
        self.id = "S" + str(Seller.nb_seller)
        super().__init__(
            type="seller",
            interaction_mode=interaction_mode,
            price_limit=price_limit,
            initial_price=initial_price,
            money=0,
            id = self.id
        )
        self.type = "seller"
        self.money = money
        if interaction_mode == None:
            raise Warning("Agent needs interaction_mode")
        self.interaction_mode = interaction_mode

        if price_limit == None:
            raise Warning("Everyone has a price!")
        self.price_limit = price_limit

        if initial_price == None:
            initial_price = self.price_limit
        initial_price = max(initial_price, self.price_limit)

    def adjust_price(self, success=None, set_price=None, edit_last=False):
        if edit_last == False:
            if set_price != None:
                self.goal_prices.append(max(set_price, self.price_limit))
            else:
                if success == None:
                    raise Warning("Need to know outcome to adjust price")
                if PRICE_ADJUST_MODE == "gauss":
                    # 1, with just a touch of variability to avoid weird states
                    adjust_amount = gauss(PRICE_ADJUST_MEAN, PRICE_ADJUST_DEV)
                if PRICE_ADJUST_MODE == "chance":
                    if random() < PRICE_ADJUST_CHANCE:
                        adjust_amount = PRICE_ADJUST_MEAN
                    else:
                        adjust_amount = 0
                if success == True:
                    self.goal_prices.append(self.goal_prices[-1] + adjust_amount)
                if success == False:

                    self.goal_prices.append(
                        max(self.goal_prices[-1] - adjust_amount, self.price_limit)
                    )
        else:
            if set_price != None:
                self.goal_prices[-1] = max(set_price, self.price_limit)
            else:
                raise Warning(
                    "Hmm. I don't think it makes sense to edit the "
                    + "last goal price based on success or failure"
                )

class Baker(Seller):

    def __init__(self,
                 bread_stock=0.0,
                 wheat_stock=0.0,
                 flour_stock=0.0,
                 water_stock=0.0,
                 money=0.0,
                 water_stock_capacity=100,
                 wheat_stock_capacity=100,
                 flour_stock_capacity=100
                 ):
        self.bread_stock = [bread_stock]
        self.wheat_stock = wheat_stock
        self.flour_stock = flour_stock
        self.water_stock = water_stock
        self.water_stock_capacity = water_stock_capacity
        self.flour_stock_capacity = flour_stock_capacity
        self.wheat_stock_capacity = wheat_stock_capacity
        # Compute price_limit and init_price
        price_limit = 1.2
        init_price = 1.2
        self.wheat_prices = []
        self.water_prices = []
        super().__init__(interaction_mode='seller_asks_buyer_decides', price_limit = price_limit, initial_price = init_price, money = money)
        self.checking_account = BankAcount(holder=self)
        self.checking_account.income(0, money)
        self.balance_at_last_price = money
        self.last_price = init_price

    def produce_flour(self):
        flour_to_produce = self.wheat_stock * 0.80
        flour_to_add = min(flour_to_produce, self.flour_stock_capacity - self.flour_stock)
        print("Flour to add",flour_to_add)
        self.flour_stock += flour_to_add
        self.wheat_stock = 0

    def produce_bread(self):
        # 500 flour for 300 water 1.66 ratio
        if self.flour_stock >= 0.500 and self.water_stock >= 0.300:
            # We can produce
            bread_to_produce = min(self.flour_stock // 0.500, self.water_stock // 0.300)
            self.bread_stock.append(self.bread_stock[-1] + bread_to_produce)
            self.flour_stock -= 0.500 * bread_to_produce
            self.water_stock -= 0.300 * bread_to_produce
            self.adjust_bread_price()

    def adjust_bread_price(self):
        bread_price_production = (self.wheat_prices[-1] * 0.80) * 0.500 + self.water_prices[-1] * 0.300
        new_price = (bread_price_production + (bread_price_production * 0.25) + (bread_price_production * 0.055) + 0.50) * 2
        if new_price < self.price_limit:
            if self.money[-1] > self.balance_at_last_price:
                self.price_limit = new_price
                self.last_price = new_price
                self.balance_at_last_price = self.money[-1]
        else:
            self.price_limit = new_price

    def can_or_should_buy_wheat(self, wheat_price_kg, wheat_price_t):
        '''
        Return if Baker should and can buy wheat

        Parameter:
        wheat_price_kg (float): Wheat price for 1 kg
        wheat_price_t (float): Wheat price for 1 t
        '''
        wheat_quantity_able_to_stock = self.wheat_stock_capacity - self.wheat_stock
        if self.has_capacity_to_buy_ton(wheat_price_t):
            wheat_quantity_able_to_buy = (self.checking_account.balance // wheat_price_t) / 1000
            quantity = min(wheat_quantity_able_to_buy, wheat_quantity_able_to_stock)
            unit = 't'
        else:
            wheat_quantity_able_to_buy = (self.checking_account.balance // wheat_price_kg)
            quantity = min(wheat_quantity_able_to_buy, wheat_quantity_able_to_stock) // WHEAT_MIN_KG_BUY_QUANTITY
            unit = 'kg'
        logging.debug('Able to buy {}{} and can stock {}'.format(wheat_quantity_able_to_buy, unit, wheat_quantity_able_to_stock))
        return unit, quantity

    def has_capacity_to_buy_ton(self, t_price):
        return self.wheat_stock_capacity - self.wheat_stock >= 1000 and t_price <= self.checking_account.balance

    def can_or_should_buy_water(self, water_price):
        # Baker can only buy by 100 units
        if self.water_stock < self.water_stock_capacity:
            return (self.money[-1] * 0.25) >= water_price #and self.water_stock // 300 <= 3
        return False
    
    def buy_wheat(self, wheat_price, unit, quantity):
        logging.debug('Baker can buy in {} ({}u for {}$)'.format(unit, quantity, wheat_price))
        if unit == 't':
            self.wheat_stock += quantity * 1000
            self.checking_account.pay(1, quantity * wheat_price)
        if unit == 'kg':
            self.wheat_stock += quantity * WHEAT_MIN_KG_BUY_QUANTITY
            self.checking_account.pay(1, quantity * wheat_price)
    
    def buy_water(self, water_price):
        water_could_buy = (self.money[-1] * 0.25) // water_price
        water_to_buy = min(self.water_stock_capacity - self.water_stock, abs(self.water_stock_capacity - water_could_buy))
        print("TO BUY", water_to_buy, water_could_buy, self.water_stock, self.water_stock_capacity)
        self.money.append(self.money[-1] - water_to_buy * water_price)
        self.water_stock += water_to_buy
        print("STOCK WATER", self.water_stock)
        self.water_prices.append(water_price)

    def sell_bread(self):
        while(self.bread_stock[-1] != 0):
            self.money.append(self.money[-1] + self.price_limit)
            self.bread_stock.append(self.bread_stock[-1] - 1)

    def __repr__(self):
        return 'Baker ({}) : {}w {}f {}wt {}$'.format(self.bread_stock[-1], self.wheat_stock, self.flour_stock, self.water_stock, self.checking_account.balance, self.price_limit)