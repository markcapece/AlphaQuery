import pandas as pd
from .customexceptions import KeyNotFoundError, SymbolNotFoundError


class FormatTable(object):
    """Base class for transforming Alphaquery responses into
    formatted dataFrames
    """

    @staticmethod
    def make_table(response_content):
        """Construct a pandas DataFrame from response content
        """
        try:
            table = pd.read_json(response_content)
            if table.index.empty:
                raise SymbolNotFoundError('Symbol not found.')
            return table
        except ValueError:
            raise KeyNotFoundError('Invalid key.')

    @staticmethod
    def clear_nan(table):
        """Remove empty columns and rows
        Overwrites current table
        """
        table.dropna(axis=1, how='all', inplace=True)
        table.dropna(axis=0, how='all', inplace=True)
        return table

    @staticmethod
    def unpack_series(table):
        """DataFrame cells contain dictionaries in the second column
        that must be extracted into separate columns
        """
        table = table[table.columns[1]]
        table = table.apply(pd.Series)
        return table

    @staticmethod
    def clean_rows(table):
        """Removes numbers in front of row headers
        """
        row_series = pd.Series([row.split(' ')[1] for row in table.index])
        table.set_index(row_series, inplace=True)
        return table

    @staticmethod
    def clean_columns(table):
        """Removes numbers in front of column headers
        Sets datatype to float
        """
        table.columns = [col.split(' ')[1] for col in table.columns]
        table = table.astype('float32')
        return table

    @staticmethod
    def first_row_as_header(table):
        """Converts the first row contents to column headers
        Removes bottom rows and sets datatype to float
        """
        table.columns = table.iloc[0]
        table = table.iloc[1:6]
        table = table.astype('float32')
        return table

    @staticmethod
    def period_columns(table, period):
        """Adds period value to column headers
        Sets datatype to float
        """
        table.columns = [col+str(period) for col in table.columns]
        table = table.astype('float32')
        return table

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return str(self)
