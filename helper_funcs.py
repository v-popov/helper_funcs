import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class HF:

    def df_preview(df: pd.DataFrame, n_samples: int = 2) -> pd.DataFrame:
        d = {'col_name': [],
             'Num Nulls': [],
             'Type': [],
             'Num Unique': [],
             'Sample Values': []}
        for col_name in df.columns:
            col = df[col_name]
            d['col_name'].append(col_name)
            d['Num Nulls'].append(col.isna().sum())
            d['Type'].append(col.dtypes)
            d['Num Unique'].append(col.unique().shape[0])
            d['Sample Values'].append(col.values[:n_samples])
        logging.info('Shape: {}'.format(df.shape))
        return pd.DataFrame(d)

    def rename_col(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
        new_columns = df.columns.values
        col_ind = list(new_columns).index(old_name)
        new_columns[col_ind] = new_name
        df.columns = new_columns
        return df

    def columns_mismatch(col_1: pd.Series, col_2: pd.Series) -> set:
        """
        :param df:
        :param col_name_1:
        :param col_name_2:
        :return: set of values from df[col_name_1] that are not present in df[col_name_2]
        """
        set_unique1 = set(col_1.unique())
        set_unique2 = set(col_2.unique())
        difference = set_unique1 - set_unique2
        logging.info('There are {} unique elements in Column_1'.format(len(set_unique1)))
        logging.info('There are {} unique elements in Column_2\n'.format(len(set_unique2)))
        logging.info('There are {} values that are present in Column_1, '
              'but not present in Column_2:\n\n{}'.format(len(difference), difference))
        return difference

    def df_difference(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
        """
        :param df1:
        :param df2:
        :return: pd.DataFrame of values that are present in df1, but not present in df2
        """
        assert df_1.shape[1] == df_2.shape[1], 'DataFrames have different number of columns'
        assert (df_1.dtypes.values == df_2.dtypes.values).all(), 'Columns type mismatch'
        col_names = ['df1_' + i + '_df2_' + j for i, j in zip(df_1, df_2)]
        df_1.columns = col_names
        df_2.columns = col_names
        return pd.concat([df_2, df_1, df_1], sort=False).drop_duplicates(keep=False)

    def verify_dates_integity(df: pd.DataFrame, date_col: str) -> None:
        dates = pd.to_datetime(df[date_col])
        date_start = df[date_col].min()
        date_end = df[date_col].max()
        date_range = pd.date_range(start=date_start, end=date_end, freq='D')
        logging.info('Start Date: {}; End Date: {}, Range Length: {}'.format(date_start, date_end, len(date_range)))
        num_missing_dates = ~np.isin(date_range, dates)
        logging.info('Number of missing dates: {}'.format(sum(num_missing_dates)))
        if sum(num_missing_dates) > 0:
            logging.info('Missing dates: {}'.format(date_range[~np.isin(date_range, dates)]))

    def duplicate(df: pd.DataFrame, how: str, n_times: int) -> pd.DataFrame:
        """
        :param df:
        :param how: either "whole" ([1,2] -> [1,2,1,2]) or "element_wise" ([1,2] -> [1,1,2,2])
        :param n_times:
        :return: extended pd.DataFrame
        """
        if how == 'whole':
            return pd.DataFrame(np.tile(df.values.T, n_times).T, columns=df.columns)
        elif how == 'element_wise':
            return pd.DataFrame(np.repeat(df.values, n_times, axis=0), columns=df.columns)

    def groupby_to_list(df: pd.DataFrame, by_cols: list, col_to_list: str) -> pd.DataFrame:
        """
        :param df: pd.DataFrame
        :param by_cols: list of column names
        :param col_to_list:
        :return: pd.DataFrame groupped by by_cols with all values of the by_cols index gathered in one cell as list
        """
        groupped = df.groupby(by_cols)
        return groupped[col_to_list].apply(list).reset_index()

    def chunkenize(data_to_split, num_chunks, df_indices=[], copy=True) -> list:
        """
        :param data: list or pd.DataFrame
        :param num_chunks: int
        :param df_indices: can be provided if type(data)==pd.DataFrame
        :param copy: Boolean, defines whether the copy of data is created, so that the data in outer scope is not affected
        :return: list of objects with the same type as data_to_split
        """
        if copy:
            data = data_to_split.copy()
        else:
            data = data_to_split

        data_length = len(data)
        chunk_length = data_length // num_chunks

        if chunk_length * num_chunks < data_length:
            chunk_length += 1

        logging.info('Splitting data into {} chunks with length {} (last chunk can be smaller)'.format(num_chunks, chunk_length))

        if isinstance(data_to_split, list):
            chunks = [data[i:i + chunk_length] for i in range(0, data_length, chunk_length)]
        elif isinstance(data_to_split, pd.DataFrame):
            if len(df_indices) > 0:
                columns = data.columns
                data.set_index(df_indices, inplace=True)
            chunks = [data[i:i + chunk_length] for i in range(0, data_length, chunk_length)]
            if len(df_indices) > 0:
                chunks = [chunk.reset_index()[columns] for chunk in chunks]
        else:
            logging.warning("Incorrect type: data should be either list or Pandas DataFrame")
            chunks = 0

        return chunks

    def filter_df(df, col_name, l_bound=None, r_bound=None, inclusive=True) -> pd.DataFrame:
        """
        :param df: pd.DataFrame to be filtered
        :param col_name: str; should be in df.columns
        :param l_bound: can be any type that matched df[col_name]; can be omitted if r_bound is specified
        :param r_bound: can be any type that matched df[col_name]; can be omitted if l_bound is specified
        :param inclusive: if False -> strict inequality; def. -> True

        :return: filtered DF
        """
        values = df[col_name]

        if (l_bound is not None) and (type(values[0]) != type(l_bound)):
            logging.warning("Left bound type {} doesn't match values type {}.".format(type(l_bound), type(values[0])))
        if (r_bound is not None) and (type(values[0]) != type(l_bound)):
            logging.warning("Right bound type {} doesn't match values type {}.".format(type(r_bound), type(values[0])))

        logging.info('Original length: {}'.format(len(df)))
        inds = np.array([True] * len(df))

        if l_bound is not None:
            if inclusive:
                inds = inds & (values >= l_bound)
            else:
                inds = inds & (values > l_bound)
        if r_bound is not None:
            if inclusive:
                inds = inds & (values <= r_bound)
            else:
                inds = inds & (values < r_bound)

        df = df[inds]
        logging.info('Resulting length: {}'.format(len(df)))

        return df
