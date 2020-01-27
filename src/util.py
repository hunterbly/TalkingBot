from tabulate import tabulate
import pandas as pd
import datetime

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

    # Change date column to string
    if('date' in df.columns):
        df['date'] = df['date'].dt.strftime('%d %b')
    
    msg = []
    for index, row in df.head().iterrows():
        temp_msg = []

        for col in df.columns:
            ele = row[col]
            temp_msg.append(str(ele))  # Join each row

        msg.append(', '.join(temp_msg))     # Append to same list

    # Join all rows
    res = '\n'.join(msg)
    
    return(res)
