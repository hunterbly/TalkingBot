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

def print_df(df, bold = None):

    ####
    # Manipulate dataframe before concat
    ####

    # Handle bold input, string/list
    if bold is not None:
        if not isinstance(bold, list):
            bold = [bold]
    else:
        bold = []
            
    # Change date column to string. Always bold date column
    if('date' in df.columns):
        df['date'] = df['date'].dt.strftime('%d %b')
        bold.append('date')

    # Add bold tag to columns
    bold_cols = list(set(bold))  # Unique list
    if (len(bold_cols) >= 1):
        df[bold_cols] = df[bold_cols].apply(lambda x: "<b>" + x + "</b>")

    ####
    # Concat dataframe to a string for telegram display
    ####
        
    msg = []
    for index, row in df.iterrows():
        temp_msg = []

        for col in df.columns:
            ele = "{}".format(str(row[col]))
            temp_msg.append(ele)  # Join each row

        msg.append(', '.join(temp_msg))     # Append to same list

    # Join all rows
    res = '\n'.join(msg)
    
    return(res)

def get_input_date(input = None):

    if not input:     # None or empty strings 
        input_str = datetime.date.today().strftime("%Y%m%d")
    else:
        if(len(input) == 4):   # Assume input in MMDD, append year
            year = datetime.date.today().year
            input_str = str(year) + str(input) 
        else:
            input_str = input  # Assume input in YYYYMMDD

    try:
       ref_date = datetime.datetime.strptime(input_str, '%Y%m%d')
       ref_str = ref_date.strftime('%Y-%m-%d')

       return(ref_str)
   
    except Exception as e:
        print(e)
        error = 'Error: Please input date in YYYYMMDD format'
        return(error)
