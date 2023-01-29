from pip._vendor import requests
from bs4 import BeautifulSoup

base = 'https://iceandfire.fandom.com/wiki/'
source = ''
cible = ''


def main(source, cible):
    """doc main"""
    print('source: ', source)
    print('cible: ', cible)


def liste_liens(page):
    """doc liste_liens(page)"""
    content = requests.get(base + page)
    # CONTENT SELECTION
    # select body in page
    soup = BeautifulSoup(content.content, 'html.parser')
    soup = soup.select('div.mw-parser-output a[href^="/wiki/"][title]')
    # LIST REDUCTION
    # get list from href
    liste = []
    for link in soup:
        liste.append(link.attrs['href'])
    # remove '/wiki/'
    for element in range(len(liste)):
        if '/wiki/' in liste[element]:
            liste[element] = liste[element].replace('/wiki/', '')
    # remove doubles
    liste = list(set(liste))
    # RETURN
    # if empty list, then there is no path, we must return None
    if not liste:
        return None
    # else, return the list
    return liste


# main('House_Lannister', 'House_Stark')
print(base + 'Petyr_Baelish')
liste_liens('Petyr_Baelish')
