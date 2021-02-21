import os
from product import Product

class Storage:
    def __init__(self):
        self.cache = {}

    def get_or_create_pending_product(self, user_id):
        user_id = str(user_id)

        if(user_id in self.cache):
            return self.cache[user_id]

        return self.create_new_pending_product(user_id)

    def create_new_pending_product(self, user_id):
        user_id = str(user_id)

        product = Product()
        self.__add_to_cache(user_id, product)

        return product

    def __add_to_cache(self, user_id, product):
        user_id = str(user_id)
        self.cache[user_id] = product
