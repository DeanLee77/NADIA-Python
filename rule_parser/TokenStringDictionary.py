from fact_value.FactValueType import FactValueType


class TokenStringDictionary:
    dictionary = {
        "No": FactValueType.INTEGER,
        "Do": FactValueType.DOUBLE,
        "De": FactValueType.DECIMAL,
        "Da": FactValueType.DATE,
        "Url": FactValueType.URL,
        "Id": FactValueType.GUID,
        "Ha": FactValueType.HASH,
        "Q": FactValueType.DEFI_STRING,
        "false": FactValueType.BOOLEAN,
        "FALSE": FactValueType.BOOLEAN,
        "False": FactValueType.BOOLEAN,
        "true": FactValueType.BOOLEAN,
        "TRUE": FactValueType.BOOLEAN,
        "True": FactValueType.BOOLEAN,
        "WARNING": FactValueType.WARNING,
        "L": FactValueType.STRING,
        "M": FactValueType.STRING,
        "U": FactValueType.STRING
    }

    @staticmethod
    def find_fact_value_type(token):
        return TokenStringDictionary().dictionary[token]

    @classmethod
    def get_all_key_and_values(cls):
        return cls.dictionary
