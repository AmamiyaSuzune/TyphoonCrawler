import requests
from bs4 import BeautifulSoup
import re

url = "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW923071506&id=202304&basin=wnp&lang=en"
response = requests.get(url)
with open("sample.txt","w") as f:
    f.write(response.text)