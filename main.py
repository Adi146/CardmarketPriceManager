#!/usr/bin/env python

from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP
from CardmarketPriceManager.CardCategory import CardCategory
from CardmarketPriceManager.utils import checkForNextSite, numCards
from CardmarketPriceManager.Exporters.Exporter import createExporters
import argparse
import yaml
import logging
import sys

parser = argparse.ArgumentParser("CardmarketPriceManager")
parser.add_argument("--configFile", type=open, default="./config.yaml")
args = parser.parse_args()

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root.addHandler(handler)

config = yaml.safe_load(args.configFile)
cardMarket = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])

postData = {"article": []}

categories = []
if "Categories" in config:
    for category in config["Categories"]:
        categories.append(CardCategory(category, cardMarket))

exporters = []
if "Exporters" in config:
    exporters = createExporters(config["Exporters"])

stock_response = cardMarket.stock_management.get_stock()
if stock_response.status_code == 307:
    stock_response = cardMarket.resolver.api.request(cardMarket.api_map["stock_management"]["get_stock"]["url"] + "/1", "get")

i = 0
while stock_response is not None and stock_response.status_code != 429:
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
                    logging.info("[" + str(i) + "/" + str(numCards(stock_response)) + " Category: " + str(
                        j + 1) + "] Card: " + stock_article["product"]["enName"] + " || New Price: " + str(
                        targetPrice) + " || Price Change: " + str(priceChange))

                    stock_article["price"] = targetPrice

                    postData["article"].append(
                        {
                            "idArticle": stock_article["idArticle"],
                            "count": stock_article["count"],
                            "price": targetPrice,
                        }
                    )
                break
        if not match:
            logging.warning("[" + str(i) + "/" + str(numCards(stock_response)) + "] Card: " + stock_article["product"][
                "enName"] + " Doesn't match any category!!!")

        if len(postData["article"]) == 100:
            cardMarket.stock_management.change_articles(data=postData)
            postData = {"article": []}

        for exporter in exporters:
            exporter.exportArticle(stock_article)

    stock_response = checkForNextSite(stock_response, cardMarket)

if (len(postData["article"])) > 0:
    cardMarket.stock_management.change_articles(data=postData)

for exporter in exporters:
    exporter.close()

