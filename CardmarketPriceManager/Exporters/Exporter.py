from abc import ABC, abstractmethod

def createExporters(config):
    exporters = []
    for exporterConfig in config:
        if exporterConfig["Exporter"]["Type"] == "CSV":
            from .CsvExporter import CsvExporter
            exporters.append(CsvExporter(exporterConfig["Exporter"])) 

    return exporters

class Exporter(ABC):

    @abstractmethod
    def exportArticle(self, article):
        pass

    @abstractmethod
    def close(self):
        pass
