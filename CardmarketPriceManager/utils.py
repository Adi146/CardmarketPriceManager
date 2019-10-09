import re

def checkForNextSite(stock_response, cardMarket):
    if stock_response.status_code == 206:
        match = re.search('(\d+)-(\d+)/(\d+)', stock_response.headers["Content-Range"])

        if int(match.group(2)) < int(match.group(3)):
            return cardMarket.resolver.api.request(cardMarket.api_map["stock_management"]["get_stock"]["url"] + "/" + str(int(match.group(2)) + 1), "get")
        else:
            return None
    else:
        return None

def numCards(stock_response):
    if stock_response.status_code == 206:
        match = re.search('(\d+)-(\d+)/(\d+)', stock_response.headers["Content-Range"])

        return int(match.group(3));
    else:
        return len(stock_response.json()["article"])