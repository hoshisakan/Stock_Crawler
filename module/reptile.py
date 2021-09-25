from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class RequestPageSource():
    """ 
        url: request base url
        mode: set True send post request, otherwise send get request
        cookies: add cookie to request, default is empty dictionary
        headers: add headers to request, example {'User-agent': 'Mozilla/5.0'}
    """
    def __init__(self, **params):
        self.__url = params['url']
        self.__mode = params['mode']
        self.__cookies = params.get('cookies', {})
        self.__headers = params.get('headers', {})
        self.__response = self.__request_mode()

    def __request_mode(self):
        if self.__mode is True:
            return requests.post(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)
        return requests.get(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)

    def __enter__(self):
        return self.__response

    def __exit__(self, type, value, traceback):
        pass
