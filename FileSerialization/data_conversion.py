#!/usr/bin/python3
import csv
import json
import logging
from enum import Enum
from abc import ABC, abstractmethod
from typing import List
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class StrEnum(str, Enum):
    pass


class FileTypes(StrEnum):
    JSON = 'json'
    XML = 'xml'
    CSV = 'csv'


class FileSerializer(ABC):

    @abstractmethod
    def serialize(self, data: List[dict], output_path: str):
        raise NotImplementedError()


class JSONSerializer(FileSerializer):

    def serialize(self, data: dict, output_path: str) -> None:
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file)


class CSVSerializer(FileSerializer):

    def serialize(self, data: List[dict], output_path: str):
        csv_data, header = [], []
        for item in data:
            if not header:
                header = list(item.keys())
                csv_data.append(header)
            row = []
            for key in header:
                if key in item:
                    if isinstance(item[key], list):
                        entities = item[key][0]
                        row.append(entities['id']), row.append(entities['name'])
                    else:
                        row.append(item[key])
                else:
                    row.append('')
            csv_data.append(row)
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)


class XMLSerializer(FileSerializer):

    def serialize(self, data, output_path):
        root = ET.Element('persons')
        for item in data:
            row_el = ET.SubElement(root, 'person')
            for item_name, item_value in item.items():
                if isinstance(item_value, list):
                    row_sub_el = ET.SubElement(row_el, item_name)
                    for entity in item_value:
                        entity_sub_el = ET.SubElement(row_sub_el, 'entity')
                        for name, value in entity.items():
                            item_sub_el = ET.SubElement(entity_sub_el, name)
                            item_sub_el.text = str(value)
                else:
                    item_el = ET.SubElement(row_el, item_name)
                    item_el.text = str(item_value)
        tree = ET.ElementTree(root)
        tree.write(output_path)


class FileDeserializer(ABC):

    @abstractmethod
    def deserialize(self, data):
        raise NotImplementedError


class CSVDeserializer(FileDeserializer):

    def deserialize(self, file_content: str) -> List[dict]:
        try:
            return [row for row in csv.DictReader(file_content.splitlines())]
        except ValueError as err:
            logger.error(err)
            raise err


class XMLDeserializer(FileDeserializer):

    def deserialize(self, file_content: str) -> List:
        try:
            root = ET.fromstring(file_content)
            persons = []
            for person in root.findall("./person"):
                person_dict = self.__parse_person(person)
                persons.append(person_dict)
            return persons
        except ValueError as err:
            print(err)

    @staticmethod
    def __parse_person(person: ET.Element) -> dict:
        person_dict = {}
        for element in person:
            if element.tag == "entities":
                entities = []
                for entity in element.findall("./entity"):
                    entity_dict = {}
                    for sub_element in entity:
                        entity_dict[sub_element.tag] = sub_element.text
                    entities.append(entity_dict)
                person_dict[element.tag] = entities
            person_dict[element.tag] = element.text
        return person_dict


class JSONDeserializer(FileDeserializer):

    def deserialize(self, file_content: str) -> dict:
        try:
            return json.loads(file_content)
        except ValueError as err:
            print(err)


class FileConverterFactory:

    @staticmethod
    def get_serializer(file_format: str) -> FileSerializer:
        if file_format == FileTypes.JSON:
            return JSONSerializer()
        elif file_format == FileTypes.CSV:
            return CSVSerializer()
        elif file_format == FileTypes.XML:
            return XMLSerializer()

        raise ValueError(f'Incorrect file format: {file_format}.')

    @staticmethod
    def get_deserializer(file_format: str) -> FileDeserializer:
        if file_format == FileTypes.JSON:
            return JSONDeserializer()
        elif file_format == FileTypes.CSV:
            return CSVDeserializer()
        elif file_format == FileTypes.XML:
            return XMLDeserializer()

        raise ValueError(f'Incorrect file format: {file_format}.')
