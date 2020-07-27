from .Exporter import Exporter
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

class GoogleSheetsExporter(Exporter):
    HEAD_LINE = [["Card", "Set", "Language", "Condition", "Foil", "Signed", "Altered", "Playset", "Rarity", "Count", "Price"]]

    def __init__(self, config):
        self.client = gspread.service_account(config["CredentialsFile"])
        self.sheet = self.client.open(config["SheetName"]).sheet1
        self.rowIndex = 1

        self.writeRow(GoogleSheetsExporter.HEAD_LINE)

    def exportArticle(self, article):
        row = [[
            article["product"]["enName"], 
            article["product"]["expansion"],
            article["language"]["languageName"],
            article["condition"],
            article["isFoil"],
            article["isSigned"],
            article["isAltered"],
            article["isPlayset"],
            article["product"]["rarity"],
            article["count"],
            article["price"]
        ]]

        self.writeRow(row)

    def writeRow(self, row):
        columnRange = string.ascii_uppercase[0] + str(self.rowIndex) + ":" + string.ascii_uppercase[len(row[0]) - 1] + str(self.rowIndex)

        self.sheet.update(columnRange, row)
        self.rowIndex += 1

    def close(self):
        pass