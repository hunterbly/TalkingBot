from tabulate import tabulate
import pandas as pd
import datetime
from src.logger import setup_logger

def stop_quietly(msg):

    """ Log the parent function and write error message to log """
    
    caller_func = inspect.stack()[1][3]
    err_msg = f"Exit in function {caller_func} - {msg}"
    logger.warning(err_msg)
    
    sys.exit("\n" + err_msg + "\n")


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

def parse_telegram_input(telegram_input, num = 1):

    """ Turn telegram input text to multiple variables """
    
    list_param = telegram_input.split()
    len_param  = len(list_param)                    # Number of parameters  
    n = len_param if num >= len_param else num      # Handle input too long

    # Python list is not inclusive
    res = tuple(list_param[1:n+1])

    # If single value return first instead of tuple
    if(len(res) == 1):
        res = res[0]
    
    return(res)

def print_history_df(df):
    
    ####
    # Print code and signal first (Group by columns)
    ####
    first_row = df.iloc[0]
    code = str(first_row['code'])
    signal = str(first_row['signal'])
    signal_index = str(first_row['signal_index'])
    header_str = (f"\n<b>{code} - {signal} ({signal_index})</b>\n")
    
    small_df = df[['date', 'day.0', 'day.1', 'day.2', 'day.3', 'day.4', 'day.5', 'success']]
    a = small_df.apply(lambda x: tabulate(x.transpose().to_frame()), axis = 1, result_type='expand')
    b = [header_str] + a.tolist()
    
    bb = '\n'.join(b)
    
    return(bb)

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

        # df_map  = pd.DataFrame(mapping, columns = ['signal', 'signal_label'])
        # # Load hit signal, map signal label
        # df_res = df.merge(df_map, on='signal', how='left')
        
        mapping_dict = {
            "s_bull_stick": "\u5927\u967d\u71ed",
            "s_bear_stick": "\u5927\u9670\u71ed",
            "s_bull_engulf": "\u5411\u597d\u541e\u566c",
            "s_bear_engulf": "\u5411\u6de1\u541e\u566c",
            "s_bull_harami": "\u5411\u597d\u8eab\u61f7\u516d\u7532",
            "s_bear_harami": "\u5411\u6de1\u8eab\u61f7\u516d\u7532",
            "s_2day_reverse_good": "\u5411\u597d\u96d9\u65e5\u8f49\u5411",
            "s_2day_reverse_bad": "\u5411\u6de1\u96d9\u65e5\u8f49\u5411",
            "s_bull_pierce": "\u66d9\u5149\u521d\u73fe",
            "s_bear_pierce": "\u70cf\u96f2\u84cb\u9802",
            "s_hammer": "\u939a\u982d",
            "s_shooting_star": "\u5c04\u64ca\u4e4b\u661f"
            
        }

        df_res = df.replace({"signal": mapping_dict})
        
    else:
        stop_quietly("Invalid input")


    return(df_res)
