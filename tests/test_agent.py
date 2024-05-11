import sys
import unittest
from models.resource import Resource
from models.agent import Buyer, Seller, Baker
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestAgents(unittest.TestCase):
    def test_create_buyer(self):
        # Test creating a buyer
        b = Buyer(interaction_mode="interaction_mode", price_limit=1)
        self.assertEqual(b.id, "B1")
        self.assertEqual(b.money, 0)
        self.assertEqual(b.age_day, 0)
        b.increase_age()
        self.assertEqual(b.age_day, 1)
        logging.info('test_create_buyer..........OK')

    def test_create_seller(self):
        # Test creating a seller
        s = Seller(interaction_mode="interaction_mode", price_limit=1)
        self.assertEqual(s.id, "S1")
        self.assertEqual(s.money, 0)
        logging.info('test_create_seller..........OK')

    def test_instance_count_increment(self):
        b1 = Buyer(interaction_mode="interaction_mode", price_limit=1)
        b2 = Buyer(interaction_mode="interaction_mode", price_limit=1)
        b3 = Buyer(interaction_mode="interaction_mode", price_limit=1)

        s1 = Seller(interaction_mode="interaction_mode", price_limit=1)
        s2 = Seller(interaction_mode="interaction_mode", price_limit=1)
        s3 = Seller(interaction_mode="interaction_mode", price_limit=1)

        self.assertEqual(b1.id, "B2")
        self.assertEqual(b2.id, "B3")
        self.assertEqual(b3.id, "B4")

        self.assertEqual(s1.id, "S2")
        self.assertEqual(s2.id, "S3")
        self.assertEqual(s3.id, "S4")
        logging.info('test_instance_count_increment..........OK')


class TestBakerAgent(unittest.TestCase):

    def test_can_buy_wheat(self):
        baker_buy_ton = Baker(money=1000, wheat_stock_capacity=1000)
        baker_buy_kg = Baker(money=1000, wheat_stock_capacity=999)
        self.assertEqual(('t', 1.0), baker_buy_ton.can_or_should_buy_wheat(1,1))
        self.assertEqual(('kg', 39), baker_buy_kg.can_or_should_buy_wheat(1, 1))
        logging.info('test_can_buy_wheat..........OK')


if __name__ == "__main__":
    unittest.main()
