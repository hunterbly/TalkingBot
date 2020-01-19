from tabulate import tabulate
import pandas as pd

def util_test():
    return("utility")

def parse_df(df):

    """ 
    parse dataframe to tabula format to be displayed in telegram 
    """
    if isinstance(df, pd.DataFrame):
        res = tabulate(df, tablefmt = "psql", headers="keys", showindex="never")
        res = "<pre>{}</pre>".format(res)
    else:
        err_msg = df
        res = err_msg
    return(res)

def print_df(df):

    for index, row in df.head().iterrows():
        print(row['signal_label'])
    return("")
