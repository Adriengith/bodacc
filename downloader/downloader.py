

import urllib.request
from bs4 import BeautifulSoup

position = 0
list_RCS = []

link = "https://echanges.dila.gouv.fr/OPENDATA/BODACC/2020/"
#  https://echanges.dila.gouv.fr/OPENDATA/BODACC/FluxHistorique/2018/


pagelink = urllib.request.urlopen(link)
soup = BeautifulSoup(pagelink, 'html.parser')

bs4_pre = soup.find('pre')
bs4_a = bs4_pre.find_all('a')

#print(bs4_a)
print(len(bs4_a))


for one_data in bs4_a:

    one_data = one_data.text

    if one_data[0:4] == "RCS-":
        list_RCS.append(one_data)


for download in list_RCS:
    position += 1
    urllib.request.urlretrieve(link + download, download)
    print(position,"/",len(list_RCS),">",download,"...")


