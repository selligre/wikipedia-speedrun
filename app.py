from pip._vendor import requests
from bs4 import BeautifulSoup
import json

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


def svg_disco(dico, fichier):
    with open(fichier, 'w') as f:
        for key, value in dico.items():
            f.write(f'{key}: {value}\n')


def svg_disco_json(dico, fichier):
    with open(fichier, 'w') as f:
        json.dump(dico, f)


def chg_disco(fichier):
    result = {}
    with open(fichier, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            result[key] = value
    return result


def chg_disco_json(fichier):
    with open(fichier, 'r') as f:
        return json.load(f)


# main('House_Lannister', 'House_Stark')
source = 'Petyr_Baelish'
liste_source = liste_liens(source)
# dict = {source: tuple(liste_liens(source))}

svg_disco_json(dict, 'fichier_cible.txt')
# print(chg_disco_json('fichier_cible.txt'))