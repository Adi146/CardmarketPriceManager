import sys
from .PriceStrategy import PriceStrategy


class CardCategory:
    languages = []
    rarities = []
    foil = "any"
    altered = "any"
    signed = "any"
    maxPrice = sys.float_info.max
    minPrice = 0.0
    priceStrategy = None

    def __init__(self, dict, cardMarket):
        if "Languages" in dict["Category"]:
            self.languages = dict["Category"]["Languages"]
        if "Rarities" in dict["Category"]:
            self.rarities = dict["Category"]["Rarities"]
        if "Foil" in dict["Category"]:
            self.foil = dict["Category"]["Foil"]
        if "Altered" in dict["Category"]:
            self.altered = dict["Category"]["Altered"]
        if "Signed" in dict["Category"]:
            self.signed = dict["Category"]["Signed"]
        if "MaxPrice" in dict["Category"]:
            self.maxPrice = dict["Category"]["MaxPrice"]
        if "MinPrice" in dict["Category"]:
            self.minPrice = dict["Category"]["MinPrice"]
        if "PriceStrategy" in dict:
            self.priceStrategy = PriceStrategy(dict["PriceStrategy"], cardMarket)

    def match(self, card):
        if len(self.languages) > 0 and card["language"]["languageName"] not in self.languages:
            return False
        if len(self.rarities) > 0 and card["product"]["rarity"] not in self.rarities:
            return False
        if self.foil != "any" and card["isFoil"] != self.foil:
            return False
        if self.altered != "any" and card["isAltered"] != self.altered:
            return False
        if self.signed != "any" and card["isSigned"] != self.signed:
            return False
        if card["price"] < self.minPrice:
            return False
        if card["price"] > self.maxPrice:
            return False

        return True
