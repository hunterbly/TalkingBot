from tabulate import tabulate
import pandas as pd
import datetime

def util_test():
    return("utility")

def random_print(row):
    test = str(row['a']) + '-' + str(row['b'])
    return(test)


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
    res = '\n' + '\n'.join(msg)
    
    return(res)

def format_input_date(input = None):

    """
    Return date input in YYYY-MM-DD string format. If input is None, return today's date

    Args:
        input (str): Date in MMDD or YYYYMMDD format. e.g. 0110 or 20200110

    Returns:
        ref_str (str): Date in string format (YYYY-MM-DD). e.g. 2020-01-20

    Example:
        ref_str = format_input_date('0120')

    Example output:
        '2020-01-20'
    """
    
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

def map_signal(df):
    
    """
    Map signal column to some utf readable names

    Args:
	df (Dataframe):
	
    Returns:
	res (Dataframe):

    Example:
	res = map_signal(df)

    Example output:


    Raise:

    TODO:
        Check column 'signal' exists first
    
    
    """
    
    if isinstance(df, pd.DataFrame):
        # Create signal mapping dataframe
        mapping = [['s_bull_stick', "\u5927\u967d\u71ed"],
                   ['s_bear_stick', "\u5927\u9670\u71ed"],
                   ['s_bull_engulf', "\u5411\u597d\u541e\u566c"],
                   ['s_bear_engulf', "\u5411\u6de1\u541e\u566c"],
                   ['s_bull_harami', "\u5411\u597d\u8eab\u61f7\u516d\u7532"],
                   ['s_bear_harami', "\u5411\u6de1\u8eab\u61f7\u516d\u7532"],
                   ['s_2day_reverse_good', "\u5411\u597d\u96d9\u65e5\u8f49\u5411"],
                   ['s_2day_reverse_bad', "\u5411\u6de1\u96d9\u65e5\u8f49\u5411"],
                   ['s_bull_pierce', "\u66d9\u5149\u521d\u73fe"],
                   ['s_bear_pierce', "\u70cf\u96f2\u84cb\u9802"],
                   ['s_hammer', "\u939a\u982d"],
                   ['s_shooting_star', "\u5c04\u64ca\u4e4b\u661f"]] 
        df_map  = pd.DataFrame(mapping, columns = ['signal', 'signal_label'])

        # Load hit signal, map signal label
        df_res = df.merge(df_map, on='signal', how='left')

    else:
        stop_quietly("Invalid input")


    return(df_res)
