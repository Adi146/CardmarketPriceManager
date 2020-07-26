import sys
from enum import Enum
from .conditionEnum import Condition
from statistics import mean


class PriceStrategyEnum(Enum):
    Lowest = 0
    Average = 1
    Highest = 2


class PriceStrategy:
    compareCardLanguage = True
    compareSellerCountry = True
    compareFoil = True
    compareSigned = True
    compareAltered = True
    conditionDeviation = 0
    quantityDeviation = 0
    minPrice = 0.0
    maxPrice = sys.float_info.max
    offset = 0
    strategy = PriceStrategyEnum.Lowest
    cardMarket = None
    userResponse = None

    def __init__(self, dict, cardMarket):
        self.cardMarket = cardMarket
        self.userResponse = cardMarket.account_management.account().json()

        if "ComparisionAttributes" in dict:
            if "CardLanguage" in dict["ComparisionAttributes"]:
                self.compareCardLanguage = dict["ComparisionAttributes"]["CardLanguage"]
            if "SellerCountry" in dict["ComparisionAttributes"]:
                self.compareSellerCountry = dict["ComparisionAttributes"]["SellerCountry"]
            if "Foil" in dict["ComparisionAttributes"]:
                self.compareFoil = dict["ComparisionAttributes"]["Foil"]
            if "Signed" in dict["ComparisionAttributes"]:
                self.compareSigned = dict["ComparisionAttributes"]["Signed"]
            if "Altered" in dict["ComparisionAttributes"]:
                self.compareAltered = dict["ComparisionAttributes"]["Altered"]
            if "ConditionDeviation" in dict["ComparisionAttributes"]:
                self.conditionDeviation = dict["ComparisionAttributes"]["ConditionDeviation"]
            if "QuantityDeviation" in dict["ComparisionAttributes"]:
                self.quantityDeviation = dict["ComparisionAttributes"]["QuantityDeviation"]

        if "TargetPrice" in dict:
            self.strategy = PriceStrategyEnum[dict["TargetPrice"]]
        if "MinPrice" in dict:
            self.minPrice = dict["MinPrice"]
        if "MaxPrice" in dict:
            self.maxPrice = dict["MaxPrice"]
        if "Offset" in dict:
            self.offset = dict["Offset"]


    def findPrice(self, card):
        article_response = self.findRelevantArticles(card)

        priceArray = list(map(lambda x: x["price"] if not x["isPlayset"] else x["price"] / 4, article_response["article"]))
        targetPrice = 0.0

        if len(priceArray) > 0:
            if self.strategy == PriceStrategyEnum.Lowest:
                if len(priceArray) > self.offset:
                    targetPrice = priceArray[0 + self.offset] - 0.01
                else:
                    targetPrice = priceArray[-1] + 0.01
            elif self.strategy == PriceStrategyEnum.Highest:
                if len(priceArray) > self.offset:
                    targetPrice = priceArray[-1 - self.offset] + 0.01
                else:
                    targetPrice = priceArray[0] - 0.01
            elif self.strategy == PriceStrategyEnum.Average:
                targetPrice = mean(priceArray)
        else:
            targetPrice = card["price"]

        if targetPrice < self.minPrice:
            targetPrice = self.minPrice
        if targetPrice > self.maxPrice:
            targetPrice = self.maxPrice

        return round(targetPrice, 2)


    def findRelevantArticles(self, card):
        article_request_params = {
            "start": 0,
            "maxResults": 1000
        }

        if type(self.compareCardLanguage) is bool and self.compareCardLanguage:
            article_request_params["idLanguage"] = card["language"]["idLanguage"]
        if self.compareFoil:
            article_request_params["isFoil"] = str(card["isFoil"]).lower()
        if self.compareSigned:
            article_request_params["isSigned"] = str(card["isSigned"]).lower()
        if self.compareAltered:
            article_request_params["isAltered"] = str(card["isAltered"]).lower()
        if Condition[card['condition']].value - self.conditionDeviation >= 0:
            article_request_params['minCondition'] = Condition(
                Condition[card['condition']].value - self.conditionDeviation).name

        article_response = self.cardMarket.market_place.articles(product=card["idProduct"], params=article_request_params).json()

        article_response["article"] = list(filter(lambda x: x["seller"]["idUser"] != self.userResponse["account"]["idUser"], article_response["article"]))

        if self.compareSellerCountry:
            article_response["article"] = list(filter(lambda x: x["seller"]["address"]["country"] == self.userResponse["account"]["country"], article_response["article"]))
        if self.compareCardLanguage is dict:
            article_response["article"] = list(filter(lambda x: x["language"]["languageName"] in self.compareCardLanguage))

        return article_response
