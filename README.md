❗❗❗ This tool does not work anylonger due to new limitations of the cardmarket API ❗❗❗

# CardmarketPriceManager
This is a tool to automatically manage prices of magic card on cardmarket.com.

# Requirements
[MKM-SDK](https://github.com/evonove/mkm-sdk)

[PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

# Usage
First of all you have to create your api tokens. To do this go to your cardmarket account and click on create app.
Chose Dedicated App and copy App Token, App Secret, Access Token and Access Secret to the following environment variables:

- MKM_APP_TOKEN
- MKM_APP_SECRET
- MKM_ACCESS_TOKEN
- MKM_ACCESS_TOKEN_SECRET

After that edit the config.yaml:

This tool categorizes cards so you can use another prize strategy for each category
Attributes for categories are:

    - Language
    - Rarities
    - Foil
    - Altered
    - Signed
    - MaxPrice
    - MinPrice
To find the correct price, this tool compares your stock with offers from other users
Attributes to compare are:

    - CardLanguage
    - SellerCountry
    - Foil
    - Signed
    - Altered
    - ConditionDeviation
There are three different price strategies: Lowest, Highest and Average.
With Lowest and Highest you can specify an offset for example you can specify that you offer your cards as 3rd cheapest seller.
Also you can specify the lowest and highest price.

See config.py for more information.

# Docker
Build image:
```
docker build -t cardmarketpricemanager:latest .
```
Run container:
```
docker run -d --name CardmarketPriceManager -e MKM_ACCESS_TOKEN='...' -e MKM_ACCESS_TOKEN_SECRET='...' -e MKM_APP_TOKEN='...' -e MKM_APP_SECRET='...' cardmarketpricemanager:latest
```
Chek logs:
```
docker container logs CardmarketPriceManager
```
# Note
This application is still work in progress. I am not responsible for any damage!

This is not an official cardmarket software. 
    
