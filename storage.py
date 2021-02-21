import os
from product import Product

class Storage:
    def __init__(self):
        self.__check_all_folders()
        self.cache = {}

    def __check_all_folders(self):
        paths = ["./storage/pending/", "./storage/products"]
        for path in paths:
            if(not os.path.exists(path)):
                os.makedirs(path)

    def create_or_get_pending_product(self, user_id):
        user_id = str(user_id)

        if(user_id in self.cache):
            return self.cache[user_id]

        pending = os.listdir("./storage/pending/")
        if not user_id in pending:
            return self.__create_new_pending_product(user_id)

        product_folder = os.listdir("./storage/pending/" + user_id)
        if not "product.json" in product_folder:
            return self.__create_new_pending_product(user_id)

        product = Product()

        fs = open("./storage/pending/" + user_id + "/product.json", "r", encoding="utf-8")
        product.import_json(fs.read())
        fs.close()

        self.__add_to_cache(user_id, product)
        return product

    def __create_new_pending_product(self, user_id):
        user_id = str(user_id)
        path = "./storage/pending/" + user_id + "/"
        os.mkdir(path)
        product = Product()
        fs = open(path + "product.json", "w", encoding="utf-8")
        fs.write(product.export_json())
        fs.close()

        self.__add_to_cache(user_id, product)
        return product

    def __add_to_cache(self, user_id, product):
        user_id = str(user_id)
        self.cache[user_id] = product
        
    
