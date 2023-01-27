from pip._vendor import requests
from bs4 import BeautifulSoup
import re

base = 'https://iceandfire.fandom.com/wiki/'
source = ''
cible = ''


def main(source, cible):
    """doc main"""
    print('source: ', source)
    print('cible: ', cible)


def liste_liens(page):
    """doc liste_liens"""
    content = requests.get(base + page)
    print(base + page)
    # dans la page
    soup = BeautifulSoup(content.text, 'html.parser')
    # dans le body

    # contient /wiki/
    soup = soup.find_all(href=re.compile('/wiki/'))
    print(len(soup))
    liste = []
    for link in soup:
        liste.append(link.get('href'))
    # enlever les doubles
    liste = list(set(liste))
    if (liste == []): return None
    return liste


# main('House_Lannister', 'House_Stark')
print(liste_liens('House_Stark'))