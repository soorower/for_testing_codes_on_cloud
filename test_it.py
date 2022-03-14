from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import json as JSON
from time import sleep
import os
import re
headers = {

'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
}

datas = {}
lists = []
data = {"limit": "25",
"listingType": "All",
"offset": '75',
"time": "1647135877532"}
url = f'https://mpapi.tcgplayer.com/v2/product/3494/latestsales'
r = requests.post(url,headers = headers,timeout = 10,json = data)
soup = bs(r.content,'html.parser')
print(soup)