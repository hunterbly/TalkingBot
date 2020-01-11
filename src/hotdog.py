import requests
import inspect

#####################################
###                               ###
### Define constant               ###
###                               ###
#####################################

CONST_ENDPOINT = '206.189.149.240'
CONST_PORT = 4000
CONST_LIBRARY = 'HotDog'

def testing():
    url = "http://206.189.149.240:4000/ocpu/library/HotDog/R/test_func/json"

    payload = {}
    headers= {}

    response = requests.request("POST", url, headers=headers, data = payload)

    res = response.text.encode('utf8')

    return(res)



def get_signal_performance(code):
  ## Get singal performance of a particular stock
  ##
  ## Args:
  ##  code (num):
  ##
  ## Returns:
  ##  res (Dataframe): 
  ##
  ## Example:
  ##   df = get_hit_signal(code = 1)

  func_name = inspect.stack()[0][3]
  
  return(func_name)
