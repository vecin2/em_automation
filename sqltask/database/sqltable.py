import re

from prettytable import PrettyTable

import sqltask


class SQLTable(object):
    def __init__(self, rows_dict=None):
        if rows_dict:
            self.rows = rows_dict
        else:
            self.rows = []

    def __getitem__(self, arg):
        return self.rows[arg]

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return self.rows.__iter__()

    def __repr__(self):
        return self.rows.__repr__()

    def __str__(self):
        prettytable = PrettyTable()
        if self.rows:
            prettytable.field_names = self.rows[0]._headers()
        for row in self.rows:
            prettytable.add_row(list(row.values()))
        return str(prettytable)

    def to_str(self):
        return str(self)

    def append(self, row):
        self.rows.append(row)

    def clone(self):
        return SQLTable(self.rows.copy())

    def column(self, column_name):
        try:
            if not self.rows:
                return []
            return [row[column_name] for row in self.rows]
        except KeyError:
            self._handle_invalid_column(column_name)

    def _handle_invalid_column(self, column_name):
        error_msg = (
            "Trying to extract column '" + column_name + "' but it doesn't exist."
        )
        if self.rows:
            column_names = self.rows[0]._headers()
            error_msg += " Did you mean any of the following " + str(column_names)
        else:
            error_msg += " Table is empty!"
        raise KeyError(error_msg)

    def find(self, expression=None, **kwargs):
        result = self.where(expression, **kwargs)
        if result:
            return result[0]
        return None

    def where(self, expression=None, **kwargs):
        result = self.clone()
        filters = self._get_filters(expression, **kwargs)
        for sqlfilter in filters:
            result = sqlfilter.apply(result)
        return result

    def _get_filters(self, expression, **kwargs):
        filters = self._get_keyvalue_filters(**kwargs)
        if expression:
            filters.append(ExpressionFilter(expression))
        return filters

    def _get_keyvalue_filters(self, **kwargs):
        filters = []
        for key in kwargs:
            value = kwargs[key]
            filters.append(KeyValueFilter(key.upper(), value))
        return filters


class SQLRow(dict):
    def __init__(self, dict_row):
        case_insensitive_dict = {}
        if type(dict_row) is dict:
            for k, v in dict_row.items():
                case_insensitive_dict[k.upper()] = v
        else:
            for key_value in dict_row:
                case_insensitive_dict[key_value[0].upper()] = key_value[1]
        dict.__init__(self, case_insensitive_dict)

    def __setitem__(self, key, value):
        dict.__setitem__(key.upper(), value)

    def __getitem__(self, key):
        if dict.__getitem__(self, key.upper()) is None:
            return "NULL"
        return dict.__getitem__(self, key.upper())

    def __repr__(self):
        return str(super().__repr__())

    def __str__(self):
        prettytable = PrettyTable()
        prettytable.field_names = self._headers()
        prettytable.add_row(list(self.values()))
        return str(prettytable)

    def _headers(self):
        return list(self.keys())


class TableFilter(object):
    def apply(self, table):
        result = SQLTable()
        for row in table:
            if self.is_valid(row):
                result.append(row)
        return result


class KeyValueFilter(TableFilter):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def is_valid(self, row):
        expression = str(self.key) + "==" + str(self.value)
        return ExpressionFilter(expression).is_valid(row)


class ExpressionFilter(TableFilter):
    def __init__(self, expression):
        self.operator = self._parse_operator(expression)
        try:
            splitted = re.split(self.operator, expression)
            self.key = splitted[0].strip()
            self.value = splitted[1].strip()
        except Exception as exception:
            raise ValueError(
                "Unable to parse expression '"
                + expression
                + "'. Expression format should be: <COLUMN_NAME> [>|>=|<|<=|==!=|=] <value>"
            )

    def _parse_operator(self, expression):
        # put first long operators then simple ones
        valid_operators = ["<=", ">=", "==", "!=", "=", "<", ">"]
        for operator in valid_operators:
            if "<>" in expression:
                break
            if operator in expression:
                return operator
        self._raise_invalid_operator(expression, valid_operators)

    def _raise_invalid_operator(self, expression, valid_operators):
        raise ValueError(
            "Invalid operator within expression '"
            + expression
            + "'. Valid operators are: "
            + str(valid_operators)
        )

    def is_valid(self, row):
        return self.key in row and Matcher.match(
            row[self.key], self.value, self.operator
        )


class Matcher(object):
    @staticmethod
    def match(value1, value2, operator="=="):
        type1 = type(value1)
        value2_cast = type1(value2)
        result = eval("value1" + operator + "value2_cast")
        if result:
            match = "Mached!"
        else:
            match = "Do not match"
        expression = (
            str(value1)
            + " ("
            + str(type(value1))
            + ") "
            + operator
            + " "
            + str(value2)
            + " ("
            + str(type(value2))
            + ")"
            + "-->"
            + match
        )
        sqltask.logger.info(expression)
        return result
