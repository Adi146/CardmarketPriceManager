from .Exporter import Exporter
import csv
import locale

class CsvExporter(Exporter):
    HEAD_LINE = ["Card", "Set", "Language", "Condition", "Foil", "Signed", "Altered", "Playset", "Rarity", "Count", "Price"]

    def __init__(self, config):
        self.csvFile = open(config["Path"], 'w', newline='')
        self.csvWriter = csv.writer(self.csvFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.csvWriter.writerow(CsvExporter.HEAD_LINE)

    def exportArticle(self, article):
        self.csvWriter.writerow(
            [
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
            ]
        )

    def close(self):
        self.csvFile.close()