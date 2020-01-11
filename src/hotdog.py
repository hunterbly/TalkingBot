import requests

def testing():
    url = "http://206.189.149.240:4000/ocpu/library/HotDog/R/test_func/json"

    payload = {}
    headers= {}

    response = requests.request("POST", url, headers=headers, data = payload)

    res = response.text.encode('utf8')

    return(res)
