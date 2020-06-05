import requests
import inspect
import urllib
import pandas as pd

#####################################
###                               ###
### Define constant               ###
###                               ###
#####################################

CONST_ENDPOINT = '206.189.149.240'
CONST_PORT = 4000
CONST_LIBRARY = 'HotDog'


def convert_dict_format(old_dict):

    """
    Convert dictionary with key in underscore format to dot foramt.
    And values to be quoted. Used for R param conversion

    Args:
      old_dict (dict): Old dictionary with underscore as key

    Returns:
      new_dict (dict): New dictionary with dot separated key and quoted values

    Example:
      old_dict = {'ref.date': '2020-01-10'}
      new_dict = convert_dict_key(old_dict)

    TODO:
      1. Based on type of values, e.g. not quote bool
    """

    new_keys = [k.replace('_', '.') for k in old_dict.keys()]
    new_values = ["'{}'".format(str(v)) for v in old_dict.values()]
    new_dict = dict(zip(new_keys, new_values))
    return(new_dict)


def json_to_df(json):

    """ json to dataframe with id column dropped """

    try:
        df = pd.read_json(json)
        df.drop(columns=['id'], axis=1, inplace=True, errors='ignore')  # drop id column if exists

        # Convert datetime columns to date
        # if 'date' in df.columns:
        #     df['date'] = df['date'].dt.date

    except:
        return(json)  # Return error message from R

    return(df)


def testing():

    url = "http://206.189.149.240:4000/ocpu/library/HotDog/R/load_hit_signal/json"

    payload = 'ref_date=%272020-01-10%27&option_only=true'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data = payload)

    res = response.text.encode('utf8')

    return(res)


def postit(method):
    def posted(*args, **kw):
        func_name = method(*args, **kw)
        url = "http://{}:{}/ocpu/library/{}/R/{}/json".format(CONST_ENDPOINT,
                                                              CONST_PORT,
                                                              CONST_LIBRARY,
                                                              func_name)

        kw = convert_dict_format(kw)
        payload = urllib.parse.urlencode(kw)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Send request to R OpenCPU server
        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.text.encode('utf8')
        # res = response.text

        df = json_to_df(res)
        return(df)
    return posted


@postit
def GetSignalPerformance(code, option_only=True, verbose=False):
    """
    Get signal history performace

    Args:
        code (str): Stock code
        option_only (bool): Specify whether the signal are for option only stocks. Default true

    Returns:
        df (Dataframe):

    Example:
        GetSignalPerformance(ref_date = '2020-01-10')
    """

    func_name = inspect.stack()[0][3]
    return(func_name)


@postit
def LoadHitSignal(ref_date, option_only=True):

    """
    Load signal hit history in database.
    Return all or option only signal with wide or long format

    Args:
        ref_date (str): Date in YYYY-MM-DD format, e.g. 2018-01-01
        option_only (bool): Specify whether the signal are for option only stocks. Default true

    Returns:
        df.signal (Dataframe): Stock price dataframe with calculated signal in the input date only

    Example:
        LoadHitSignal(ref_date = '2020-01-10')
    """

    func_name = inspect.stack()[0][3]
    return(func_name)


@postit
def check_cronjob():

    """
    Return the latest date of records in the cronjob tables

    Args:
      None

    Returns:
      df.res (Dataframe): Dataframe of latest date of cronjob tables

    Example:
      df.res = check_cronjob()
    """

    func_name = inspect.stack()[0][3]
    return(func_name)
