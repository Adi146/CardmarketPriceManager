from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP
from CardMarketPriceManager.config import getConfig

from CardMarketPriceManager.CardCategory import CardCategory

config = getConfig()
cardMarket = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])

priceChanges = []
newStockPrices = []
oldStockPrices = []

postData = {"article": []}

categories = []
for category in config["Categories"]:
    categories.append(CardCategory(category, cardMarket))

stock_response = cardMarket.stock_management.get_stock().json()
for i, stock_article in enumerate(stock_response["article"]):
    match = False
    for j, category in enumerate(categories):
        if category.match(stock_article):
            match = True
            targetPrice = category.priceStrategy.findPrice(stock_article)
            priceChange = round(targetPrice - stock_article["price"], 2)

            if priceChange != 0.0:
                print("[" + str(i + 1) + "/" + str(len(stock_response["article"])) + " Category: " + str(j + 1) + "] Card: " + stock_article["product"]["enName"] + " || New Price: " + str(targetPrice) + " || Price Change: " + str(priceChange))

                postData["article"].append(
                    {
                        "idArticle": stock_article["idArticle"],
                        "count": stock_article["count"],
                        "price": targetPrice,
                    }
                )
            break
    if not match:
        print("[" + str(i + 1) + "/" + str(len(stock_response["article"])) + "] Card: " + stock_article["product"]["enName"] + " Doesn´t match any category!!!")

    if len(postData["article"]) == 100:
        cardMarket.stock_management.change_articles(data=postData)
        postData = {"article": []}

if (len(postData["article"])) > 0:
    cardMarket.stock_management.change_articles(data=postData)
