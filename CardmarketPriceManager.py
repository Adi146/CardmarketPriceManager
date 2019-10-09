#!/usr/bin/env python

from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP
from CardMarketPriceManager.CardCategory import CardCategory
from CardMarketPriceManager.utils import checkForNextSite, numCards
import argparse
import yaml

parser = argparse.ArgumentParser("CardmarketPriceManager")
parser.add_argument("--configFile", type=open, default="./config.yaml")
args = parser.parse_args()

config = yaml.safe_load(args.configFile)
cardMarket = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])

priceChanges = []
newStockPrices = []
oldStockPrices = []

postData = {"article": []}

categories = []
for category in config["Categories"]:
    categories.append(CardCategory(category, cardMarket))

stock_response = cardMarket.stock_management.get_stock()
if stock_response.status_code == 307:
    stock_response = cardMarket.resolver.api.request(cardMarket.api_map["stock_management"]["get_stock"]["url"] + "/1", "get")

i = 0
while stock_response is not None:
    stock_json = stock_response.json()

    for stock_article in stock_json["article"]:
        match = False
        i += 1

        for j, category in enumerate(categories):
            if category.match(stock_article):
                match = True
                targetPrice = category.priceStrategy.findPrice(stock_article)
                priceChange = round(targetPrice - stock_article["price"], 2)

                if priceChange != 0.0:
                    print("[" + str(i) + "/" + str(numCards(stock_response)) + " Category: " + str(
                        j + 1) + "] Card: " + stock_article["product"]["enName"] + " || New Price: " + str(
                        targetPrice) + " || Price Change: " + str(priceChange))

                    postData["article"].append(
                        {
                            "idArticle": stock_article["idArticle"],
                            "count": stock_article["count"],
                            "price": targetPrice,
                        }
                    )
                break
        if not match:
            print("[" + str(i) + "/" + str(numCards(stock_response)) + "] Card: " + stock_article["product"][
                "enName"] + " Doesn't match any category!!!")

        if len(postData["article"]) == 100:
            cardMarket.stock_management.change_articles(data=postData)
            postData = {"article": []}

    stock_response = checkForNextSite(stock_response, cardMarket)

if (len(postData["article"])) > 0:
    cardMarket.stock_management.change_articles(data=postData)

