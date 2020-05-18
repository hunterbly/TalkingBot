import requests


def send_telegram_message(msg):

    """ Utility to send message to telegram groups """

    base_url = "https://api.telegram.org/bot589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g/sendMessage"
    chat_id_one = "-294841384"  # Signal Testing
    chat_id_two = "-464227511"  # Signal Development
    msg = msg

    url_one = f"{base_url}?chat_id={chat_id_one}&text={msg}"
    url_two = f"{base_url}?chat_id={chat_id_two}&text={msg}"

    payload = {}
    headers = {}

    # Send message to both groups
    requests.request("POST", url_one, headers=headers, data=payload)
    requests.request("POST", url_two, headers=headers, data=payload)

    return(None)


if __name__ == '__main__':
    send_telegram_message("ABC DEF")
