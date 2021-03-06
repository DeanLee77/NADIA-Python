from enum import Enum


class FactValueType(Enum):
        BOOLEAN = "BOOLEAN"
        INTEGER = "INTEGER"
        DEFI_STRING = "DEFI_STRING"
        TEXT = "TEXT"
        STRING = "STRING"
        DOUBLE = "DOUBLE"
        NUMBER = "NUMBER"
        DATE = "DATE"
        DECIMAL = "DECIMAL"
        LIST = "LIST"
        RULE = "RULE"
        RULE_SET = "RULE_SET"
        OBJECT = "OBJECT"
        UNKNOWN = "UNKNOWN"
        URL = "URL"
        HASH = "HASH"
        GUID = "GUID"
        NULL = "NULL"
        WARNING = "WARNING"

        @staticmethod
        def get_all_values():
                return list(map(lambda c: c.value, FactValueType))

        @staticmethod
        def get_all_enums():
                return list(map(lambda c: c, FactValueType))
