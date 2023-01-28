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
    """doc liste_liens(page)"""
    content = requests.get(base + page)
    print(base + page)
    # CONTENT SELECTION
    # select body in page
    soup = BeautifulSoup(content.text, 'html.parser').find('body')
    # that contains /wiki/
    soup = soup.find_all(href=re.compile('/wiki/'))
    # LIST REDUCTION
    # get list from href
    liste = []
    for link in soup:
        liste.append(link.get('href'))
    print('len(l) with href ' + str(len(liste)))
    print(liste)
    # remove 'https://iceandfire.fandom.com'
    for element in range(len(liste)):
        if 'https://iceandfire.fandom.com' in liste[element]:
            liste[element] = liste[element].replace('https://iceandfire.fandom.com', '')
    print('len(l) without https ' + str(len(liste)))
    print(liste)
    # remove elements from another website
    for element in range(len(liste) - 1):
        if 'https' in liste[len(liste) - element - 1]:
            liste.pop(element)
    print('len(l) without foreign pages ' + str(len(liste)))
    print(liste)
    # remove elements with ':' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if ':' not in element]
    print('len(l) without ":" ' + str(len(liste)))
    print(liste)
    # remove elements with 'POV' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if 'POV' not in element]
    print('len(l) without "POV" ' + str(len(liste)))
    print(liste)
    # remove elements with '=' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if '=' not in element]
    print('len(l) without "=" ' + str(len(liste)))
    print(liste)
    # remove elements with 'community'
    liste = [element for element in liste if 'community' not in element]
    print('len(l) without "community" ' + str(len(liste)))
    print(liste)
    # remove '/wiki/'
    for element in range(len(liste)):
        if '/wiki/' in liste[element]:
            liste[element] = liste[element].replace('/wiki/', '')
    print('len(l) without "/wiki/" ' + str(len(liste)))
    print(liste)
    # remove doubles
    liste = list(set(liste))
    print('len(l) without doubles ' + str(len(liste)))
    print(liste)
    # RETURN
    # if empty list, then there is no path, we must return None
    if not liste:
        return None
    # else, return the list
    return liste


# main('House_Lannister', 'House_Stark')
liste_liens('Petyr_Baelish')
