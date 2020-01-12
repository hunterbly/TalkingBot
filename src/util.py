from tabulate import tabulate

def util_test():
    return("utility")

def parse_df(df):

    ## parse dataframe to tabula format to be displayed in telegram

    res = tabulate(df, tablefmt = "psql", headers="keys", showindex="never")
    res = "<pre>{}</pre>".format(res)
    return(res)
