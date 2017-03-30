import csv
import json
from abc import ABC, abstractmethod


def csv_load(file: object) -> str:
    loader = csv.reader(file)
    res = ''
    for item in loader:
        res += item[0] + '\n'
        res = res.replace(';', ' ').rstrip()
        return res


def csv_save(s: str, file: object) -> None:
    s = s.split(" ")
    writer = csv.writer(file, delimiter=";", escapechar=None, quoting=csv.QUOTE_NONE, lineterminator='')
    writer.writerow(s)


def json_load(file: object) -> str:
    return '\n'.join(json.load(file)['rows'])


def json_save(s: str, file: object) -> None:
    s = s.split("\n")
    json.dump({'rows': s}, file, separators=(',', ': '))


class AbstractConverterFabric(ABC):
    @abstractmethod
    def create_converter(self, _from: str, _to: str) -> object:
        raise NotImplemented


class AbstractConverter(ABC):
    @abstractmethod
    def load(self, file: object) -> object:
        raise NotImplemented

    @abstractmethod
    def save(self, s: str, file: object) -> object:
        raise NotImplemented


class ConverterFabric(AbstractConverterFabric):

    def create_converter(self, _from: str, _to: str) -> object:
        if _from == 'json':
            load = json_load
        if _from == 'csv':
            load = csv_load

        if _to == 'json':
            save = json_save
        if _to == 'csv':
            save = csv_save
        return type('Converter', (AbstractConverter,), {'load': load, 'save': save})

