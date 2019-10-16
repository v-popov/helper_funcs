# Functionality Guide
This module provides a handful of functions to simplify the typical data processing operations and simplifying data verification procedures.

## Dependencies
* `numpy 1.17.1`
* `pandas 0.25.1`

## Methods

* ###`df_preview(df, n_samples)`

    ***Description***
    
    Creates a nice summary table of your DataFrame.
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame you want to create a preview for.
           
    * **`n_samples`: int, optional (default = 2)**
    
        Number of unique values from each column to be displayed.
    
    ***Returns***
    
    * pandas.DataFrame containing the summary information about the passed DataFrame.
    

* ###`rename_col(df, old_name, new_name)`

    ***Description***
    
    Renames the specified column.
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame you want to create a preview for.
           
    * **`old_name`: str**
    
        Name of existing `df` column to be renamed.
        
    * **`new_name`: str**
    
        Name which will replace the `old_name` column name.
    
    ***Returns***
    
    * pandas.DataFrame with the renamed column.
    
    
* ###`columns_mismatch(col_1, col_2)`

    ***Description***
    
    Extracts values that are present in `col_1`, but not in `col_2`.
    
    ***Parameters***
    
    * **`col_1`: pandas.Series**
    
        The Series you want to subtract values from.
           
    * **`col_2`: pandas.Series**
    
        The Series which is subtracted from `col_1`.
        
    Note: The word "subtract" is used not in arithmetical sense, but in a set difference sense.
    
    ***Returns***
    
    * Set with values which `col_1` contains and `col_2` does not contain.
    

* ###`df_difference(df_1, df_2)`

    ***Description***
    
    Extracts rows that are present in `df_1`, but not in `df_2`. 
    
    Note: `df_1` and `df_2` can have different column names, but number of columns should match.
    
    ***Parameters***
    
    * **`df_1`: pandas.DataFrame**
    
        The DataFrame you want to subtract values from.
           
    * **`df_2`: pandas.DataFrame**
    
        The DataFrame which is subtracted from `df_1`.
        
    Note: The word "subtract" is used not in arithmetical sense, but in a set difference sense.
    
    ***Returns***
    
    * pandas.DataFrame with rows which `df_1` contains and `df_2` does not contain.
    
    
* ###`verify_dates_integity(df, date_col)`

    ***Description***
    
    Checks whether there are any missing dates between earliest and latest dates from `df[date_col]`
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame which after selecting values from `date_col` will be verified for integrity
           
    * **`date_col`: str**
    
        Name of `df` column that will be verified for integrity
       
       
* ###`duplicate(df, how, n_times)`

    ***Description***
    
    Extends the specified DataFrame by repeating its rows.
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame which rows you want to repeat
           
    * **`how`: str**
    
        Strategy for repeating. Should be either 'whole' (then [1,2] -> [1,2,1,2]) or
        'element_wise' (then [1,2] -> [1,1,2,2])
        
    * **`n_times`: int**
    
        Number of repetitions of each row
    
    ***Returns***
    
    * Extended pandas.DataFrame with repeated rows
    
    
* ###`groupby_to_list(df, by_cols, col_to_list)`

    ***Description***
    
    Extracts values of `col_to_list` column that correspond to the same values in 
    `by_cols` column(s) and put them to list.
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame which you want to use
           
    * **`by_cols`: list of str**
    
        Column names that will be used as keys in `df`
        
    * **`col_to_list`: str**
    
        Column name which values will be put to lists
    
    ***Returns***
    
    * pandas.DataFrame with columns [`by_cols`, `col_to_list`] so that all the values in
    `col_to_list` column are lists.
    
    
* ###`chunkenize(data_to_split, num_chunks, df_indices, copy)`

    ***Description***
    
    Splits the `data_to_split` into list with `num_chunks` chunks. Can be helpful when preparing 
    data for parallel processing.
    
    ***Parameters***
    
    * **`data_to_split`: pandas.DataFrame or list**
    
        The DataFrame which you want to split in chunks
           
    * **`num_chunks`: int**
    
        Number of chunks that your data will be split in
        
    * **`df_indices`: list of str, optional (default = [])**
    
        This can be used when `data_to_split` is pandas.DataFrame. These column will be used
        as DataFrame index before splitting and will be reset afterwards.
        
    * **`copy`: bool, optional (default = True)**
    
        Determines whether you want to perform splitting on a copy of `data_to_split`.
    
    ***Returns***
    
    * List of `num_chunks` chunks that have same type as `data_to_split`.


* ###`filter_df(df, col_name, l_bound, r_bound, inclusive)`

    ***Description***
    
    Filters the `df` DataFrame `col_name` column so that it contains only records
    that corresponds to `df`[`col_name`] values in the range between `l_bound` and `r_bound`.
    
    ***Parameters***
    
    * **`df`: pandas.DataFrame**
    
        The DataFrame which column `col_name` you want to filter
           
    * **`col_name`: str**
    
        Column name from `df` which values you want to filter `df` on
        
    * **`l_bound`: same type as values of `df`[`col_name`]**
    
        Left bound of the filtered values range. Can be omitted if `r_bound` is specified
        
    * **`r_bound`: same type as values of `df`[`col_name`]**
    
        Right bound of the filtered values range. Can be omitted if `l_bound` is specified
        
    * **`inclusive`: bool, optional (default = True)**
    
        Determines whether you want range to be inclusive (True) or exclusive (False)
    
    ***Returns***
    
    * Filtered pandas.DataFrame