#!/usr/bin/python3

import logging
from argparse import ArgumentParser
from datetime import datetime
from sys import argv
from typing import Tuple, List, Optional

from data_conversion import FileConverterFactory
from data_validator import PersonSchema

logger = logging.getLogger(__name__)


class MyCustomerException(Exception):
    pass


# def parse_arguments(argv: List[str]) -> Tuple[str, ...]:
def parse_arguments(argv: List[str]) -> Tuple[str, str, str, str]:
    parser = ArgumentParser(description="Mapping: for the File serialization")
    parser.add_argument("-sf", "--sourceFormat", help="the input file format", required=True, type=str)
    parser.add_argument("-tf", "--targetFormat", help="the output file format", required=True, type=str)
    parser.add_argument("-sp", "--sourceFilePath", help="the source file path", required=True, type=str)
    parser.add_argument("-op", "--outputFilePath", help="the output file path", required=False, type=str)
    args = parser.parse_args()
    return args.sourceFormat.lower(), args.targetFormat.lower(), args.sourceFilePath, args.outputFilePath


def read_source_file(file_path: str) -> str:
    """Reads the file
    Args:
        file_path: the file path
    Returns:
        the file content
    """
    try:
        with open(file_path) as file:
            return file.read()
    except FileNotFoundError as err:
        logger.error(err)
        # raise err
        # raise MyCustomerException() from err


def generate_output_filename(file_extension: str) -> str:
    """Generates the output filename using current datetime
    Args:
        file_extension: the file extension
    Returns:
        the output filename
    """
    current_datetime = datetime.now()
    return f"result-{current_datetime.strftime('%Y-%m-%d-%H:%M:%S')}.{file_extension}"


def validate_input_data(data: list, person_schema: PersonSchema) -> None:
    """Validates the input data data
    Args:
        data: the input data
        person_schema: the instance of PersonSchema class
    Returns:
        None
    """
    for person in data:
        errors = person_schema.validate(person)
        if errors:
            logger.error(errors)


def main() -> None:
    source_format, target_format, source_file_path, output_file_path = parse_arguments(argv[1:])

    # reads the source file
    source_file_data = read_source_file(source_file_path)
    breakpoint()
    file_deserializer = FileConverterFactory.get_deserializer(source_format)
    file_content = file_deserializer.deserialize(source_file_data)

    # validates the input data
    person_schema = PersonSchema()
    validate_input_data(file_content, person_schema)

    # checks the output filename
    if not output_file_path:
        output_file_path = generate_output_filename(target_format)

    file_serializer = FileConverterFactory.get_serializer(target_format)
    file_serializer.serialize(file_content, output_file_path)


if __name__ == "__main__":
    main()
