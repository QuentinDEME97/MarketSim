from random import random, gauss
from constants.const import *
import math
import logging
import uuid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class QuantityManager:

    def __init__(self, holder=None, balance=0, label='QuantityManager', unit=''):
        if holder is None:
            raise RuntimeWarning('Stock should have a holder')
        self.holder = holder
        self.balance = balance
        self.transactions = []
        self.label = label
        self.unit = unit
        self.id = uuid.uuid4()

    def add(self, period, amount):
        if period is None or amount is None:
            raise RuntimeError('Period and amound should not be None')
        self.balance += amount
        self.transactions.append((period, amount))

    def remove(self, period, amount):
        if period is None or amount is None:
            raise RuntimeError('Period and amound should not be None')
        self.balance -= amount
        self.transactions.append((period, -amount))

    def get_last_add(self):
        last_positive = None
        for period, amount in reversed(self.transactions):
            if amount > 0:
                last_positive = (period, amount)
        return last_positive

    def get_last_remove(self):
        last_negative = None
        for period, amount in reversed(self.transactions):
            if amount < 0:
                last_negative = (period, amount)
        return last_negative

    def __repr__(self):
        return '{} balance: {}{} number_of_transactions: {}'.format(self.id, self.balance, self.unit, len(self.transactions))
class Stock(QuantityManager):

    def __init__(self, holder=None, balance=0, quantity_label='Stock', unit='u'):
        super().__init__(holder=holder, balance=balance, label=quantity_label, unit=unit)

    def add_to_stock(self, period, amount):
        super().add(period, amount)

    def remove_from_stock(self, period, amount):
        super().remove(period, amount)


class BankAcount(QuantityManager):

    def __init__(self, holder=None, balance=0, quantity_label='Stock', unit='u'):
        super().__init__(holder=holder, balance=balance, label=quantity_label, unit=unit)

    def income(self, period, amount):
        super().add(period, amount)

    def pay(self, period, amount):
        super().remove(period, amount)

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
        self.bread_stock = Stock(holder=self, quantity_label='Breads')
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
        logging.debug('Can produce {}kg flour'.format(flour_to_add))
        self.flour_stock += flour_to_add
        self.wheat_stock = 0

    def produce_bread(self):
        # 500 flour for 300 water 1.66 ratio
        if self.flour_stock >= 0.500 and self.water_stock >= 0.300:
            # We can produce
            bread_to_produce = min(self.flour_stock // 0.500, self.water_stock // 0.300)
            self.bread_stock.add_to_stock(self.age_day, bread_to_produce)
            self.flour_stock -= 0.500 * bread_to_produce
            self.water_stock -= 0.300 * bread_to_produce
            self.adjust_bread_price()

    def adjust_bread_price(self):
        '''
        Report the production price on the sell price.

        We need to check how many bread we produce and for what price.
        '''
        last_bread_produced = self.bread_stock.get_last_add()[1]
        production_cost = ((last_bread_produced * BREAD_FLOUR_NEEDED) / 0.80) * self.wheat_prices[-1] + (last_bread_produced * BREAD_WATER_NEEDED) * self.water_prices[-1]
        logging.debug('Production cost total is {} and {} for 1'.format(production_cost, production_cost/last_bread_produced))
        production_cost = (production_cost / last_bread_produced)
        bread_price_ht = production_cost + production_cost * 0.25 + 1.15
        bread_price_ttc = bread_price_ht + bread_price_ht * 0.055
        logging.debug('The price is {}'.format(bread_price_ttc))
        self.price_limit = bread_price_ttc



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
        water_quantity_able_to_stock = self.water_stock_capacity - self.water_stock
        water_quantity_able_to_buy = (self.checking_account.balance // water_price)
        quantity = min(water_quantity_able_to_buy, water_quantity_able_to_stock)
        unit = 'l'
        logging.debug(
            'Able to buy {}{} and can stock {}'.format(water_quantity_able_to_buy, unit, water_quantity_able_to_stock))
        return unit, quantity
    
    def buy_wheat(self, wheat_price, unit, quantity):
        logging.debug('Baker can buy in {} ({}u for {}$)'.format(unit, quantity, wheat_price))
        if quantity != 0:
            if unit == 't':
                self.wheat_stock += quantity * 1000
                self.checking_account.pay(self.age_day, quantity * wheat_price)
                self.wheat_prices.append(wheat_price / quantity * 1000)
            if unit == 'kg':
                self.wheat_stock += quantity * WHEAT_MIN_KG_BUY_QUANTITY
                self.checking_account.pay(self.age_day, quantity * wheat_price)
                self.wheat_prices.append(wheat_price / (quantity * WHEAT_MIN_KG_BUY_QUANTITY))
            logging.debug('Wheat price for 1 unit is {}'.format(self.wheat_prices[-1]))
    
    def buy_water(self, water_price, unit, quantity):
        logging.debug('Baker can buy in {}{} for {}$ (total of {})'.format(quantity, unit, water_price, quantity * water_price))
        self.water_stock += quantity
        self.checking_account.pay(self.age_day, quantity * water_price)
        self.water_prices.append(water_price)

    def sell_bread(self):
        to_get_on_account = self.price_limit - (self.price_limit * 0.055) - 1.15
        self.checking_account.pay(self.age_day, to_get_on_account)
        self.bread_stock.remove(self.age_day, 1)

    def __repr__(self):
        return 'Baker ({}) : {}w {}f {}wt {}$'.format(self.bread_stock.balance, self.wheat_stock, self.flour_stock, self.water_stock, self.checking_account.balance, self.price_limit)