import requests
from bs4 import BeautifulSoup
load_url_array = []
load_url = "https://www.uta-net.com/search/?Aselect=1&Keyword=creepy+nuts&Bselect=3&x=0&y=0"

html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
title = soup.select('.side.td1 a')

for elem in title:
    # print(elem.get('href'))
    if len(str(elem.get('href'))) < 20:
        load_url_array.append("https://www.uta-net.com"+str(elem.get('href')))


load_url = "https://www.uta-net.com/song/234130/"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
kasi = soup.find(id="kashi_area")
print(kasi.getText())
with open("myfile.txt", mode='w') as f:
    for load_url in load_url_array:
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")
        kasi = soup.find(id="kashi_area")
        print(kasi.getText())
        f.writelines(kasi.getText())
