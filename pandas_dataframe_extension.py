import logging
from abc import abstractmethod

import pandas as pd

logger = logging.getLogger(__name__)


# This is (partly) a copy from:
# https://github.com/Amsterdam-Data-Collective/adc-pipeline/tree/2b590e6cca41c36d7b667c707670b6c6d78ed9a2
class MlSeries(pd.Series):
    """
    This class is an extension of the Pandas DataFrame class, to provide extra functionality. In order to let this class
    work correctly, there are a few Pandas methods and properties that need to be implemented as specified by the docs.
    These methods are highlighted with comments.

    Docs: https://pandas.pydata.org/pandas-docs/stable/development/extending.html
    """

    ###
    # PANDAS METHODS
    ###

    @property
    def _constructor(self):
        """
        A lot of methods in the DataFrame class return a Series using the _constructor method.
        Every time a new Series is created, we return our Series instead of a Pandas Series.
        """
        ###
        # NOTE:
        # For now the same as Pandas Series
        # If custom methods are needed, uncomment the following line:
        # return MlSeries
        ###
        return pd.Series

    ###
    # CUSTOM METHODS AND PROPERTIES
    ###

    # PLACEHOLDER: Nothing is added for series yet, add functionality here and delete this comment.


class MlDataFrame(pd.DataFrame):
    """
    This class is an extension of the Pandas DataFrame class, to provide extra functionality. In order to let this class
    work correctly, there are a few Pandas methods and properties that need to be implemented as specified by the docs.
    These methods are highlighted with comments.

    Docs: https://pandas.pydata.org/pandas-docs/stable/development/extending.html
    """

    ###
    # PANDAS METHODS
    ###

    @property
    def _constructor_expanddim(self):
        """Abstract method of the Pandas DataFrame class: just calls super class."""
        return super()._constructor_expanddim(self)

    @property
    @abstractmethod
    def _constructor(self):
        """
        A lot of methods in the DataFrame class return a DataFrame using the _constructor method.
        Every time a new DataFrame is created, we return the our DataFrame instead of a Pandas DataFrame.
        """
        return MlDataFrame

    @property
    @abstractmethod
    def _constructor_sliced(self):
        """When slicing methods are called, return custom (inherited) Series object"""
        return MlSeries

    ###
    # CUSTOM METHODS AND PROPERTIES
    ###

    @property
    def pandas_df(self) -> pd.DataFrame:
        """
        Returns:
            Casted Pandas Dataframe from MlDataFrame
        """
        return pd.DataFrame(self)

    @property
    def memory_size(self) -> float:
        """
        Returns:
            Memory size of the full DataFrame in KB
        """
        return round(self.memory_usage().sum() / 1000, 2)
