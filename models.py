from pymongo import MongoClient
from config import config

class RecipeModel:
    def __init__(self):
        print(config['dev'].DB_URI)
        client = MongoClient(config['dev'].DB_URI, maxPoolSize=50, wtimeOut=2500, serverSelectionTimeoutMS=5000)
        self.db = client[config['dev'].DB_NAME]

    def get_recipes(self, ingredients):
        ing_string = ' '.join(ingredients)
        print(ing_string)
        recipes = list(self.db.recipes.find({"$text":{"$search":ing_string}},
                                            {"score":{"$meta":"textScore"}})
                       .sort([("score",{"$meta":"textScore"})])
                       .limit(10))
        print(recipes)
        return recipes