import logging
from typing import List, Union

import numpy as np

import pandas as pd

logger = logging.getLogger(__name__)


# This is (partly) a copy from:
# https://github.com/Amsterdam-Data-Collective/adc-pipeline/tree/2b590e6cca41c36d7b667c707670b6c6d78ed9a2
def memory_size(df) -> float:
    """
    Returns:
        Memory size of the full DataFrame in KB
    """
    return round(df.memory_usage().sum() / 1000, 2)


def downcast(df, signed_cols: List[str] = None) -> pd.DataFrame:
    """
    Automatically check for signed/unsigned columns and downcast.
    However, if a column can be signed while all the data in that column is unsigned, you don't want to downcast to
    an unsigned column. You can explicitly pass these columns.

    :arg df: Data as Pandas DataFrame
    :arg signed_cols: List of signed columns (signed = positive and negative values, unsigned = only positive values).
    """
    logger.info(f'Size before downcasting: {df.memory_size} KB')
    for column in df.columns:
        if df[column].dtype in [np.int8, np.int16, np.int32, np.int64]:
            if (df[column] < 0).any() or (signed_cols is not None and df[column].name in signed_cols):
                df[column] = pd.to_numeric(df[column], downcast='signed')
            else:
                df[column] = pd.to_numeric(df[column], downcast='unsigned')
        elif df[column].dtype in [np.float16, np.float32, np.float64]:
            df[column] = pd.to_numeric(df[column], downcast='float')
    logger.info(f'Size after downcasting: {df.memory_size} KB')

    return df


def reorder_columns(df, columns: Union[str, List[str]], index: int) -> pd.DataFrame:
    """
    Move/reorder a single column or a list of columns to a new index.

    :arg df: Data as Pandas DataFrame
    :arg columns: Columns to move to a new index.
    :arg index: Index where the column(s) will be moved to.
    """
    data_to_be_moved = df[columns]
    df.drop(columns=columns, inplace=True)
    if isinstance(columns, list):
        for column in columns:
            df.insert(index, column, data_to_be_moved[column])
            index += 1
    else:
        df.insert(index, columns, data_to_be_moved)

    return df


def drop_columns_with_single_value(df, skip_columns: Union[str, List[str]] = None) -> pd.DataFrame:
    """
    Drop all columns containing only a single value. This includes all columns that only contain NaN/None.

    :arg df: Data as Pandas DataFrame
    :arg skip_columns: Columns to skip
    """
    columns_to_drop = []
    for column in list(df.columns):
        if skip_columns is not None and column in skip_columns:
            continue
        elif len(df[column].unique()) <= 1:
            columns_to_drop.append(column)
    df = df.drop(columns=columns_to_drop)

    if not columns_to_drop:
        logger.info('No columns were dropped, could not find a column with only a single value (incl. NaN/None)')
    else:
        logger.info(f'Columns dropped containing only a single value (incl. NaN/None): '
                    f'{", ".join(str(column) for column in columns_to_drop)}')

    return df


def factorize_columns(df, columns: Union[str, List[str]]) -> pd.DataFrame:
    """
    Convert columns to a list of unique integers per category

    :arg df: Data as Pandas DataFrame
    :arg columns: Columns to convert to a list of unique integers per category
    """
    if not isinstance(columns, list):
        columns = [columns]

    for column in columns:
        df[column], _ = pd.factorize(df[column])

    return df


def keep_top_items_in_columns(df, columns: Union[str, List[str]], number_of_items: int) -> pd.DataFrame:
    """
    For all the columns passed in the arguments, keep the N-top frequent items. The rest will be set to 'other'.
    :arg df: Data as Pandas DataFrame
    :arg columns: Columns to only keep N-top frequent items.
    :arg number_of_items: The top number of items to keep (= N).
    """
    if not isinstance(columns, List):
        columns = [columns]

    for column in columns:
        counter_list = df[column].value_counts()
        top_items_list = counter_list[:number_of_items].index.tolist()
        df[column].loc[~np.array(df[column].isin(top_items_list))] = 'other'

    return df
