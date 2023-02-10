from pip._vendor import requests
from bs4 import BeautifulSoup
import json

BASE = 'https://iceandfire.fandom.com/wiki/'


def main(source_str, cible_str):
    """doc main"""
    print('source: ', source_str)
    print('cible: ', cible_str)


def liste_liens(page):
    """doc liste_liens(page)"""
    content = requests.get(BASE + page)
    # CONTENT SELECTION
    soup = BeautifulSoup(content.content, 'html.parser')
    soup = soup.select('div.mw-parser-output a[href^="/wiki/"][title]')
    # LIST REDUCTION
    liste = []
    for link in soup:
        liste.append(link.attrs['href'])
    # remove '/wiki/'
    for element in range(len(liste)):
        if '/wiki/' in liste[element]:
            liste[element] = liste[element].replace('/wiki/', '')
    # remove elements with impurities
    liste = [element for element in liste if ':' not in element]
    # remove doubles
    liste = list(set(liste))
    # RETURN
    # if not liste:
    #     return None
    return liste


def svg_dico(dico, fichier):
    with open(fichier, 'w') as f:
        for key, value in dico.items():
            f.write(f'{key}: {value}\n')


def svg_dico_json(dico, fichier):
    with open(fichier, 'w') as f:
        json_str = json.dumps(dico, indent=4)
        f.write(json_str)


def chg_dico(fichier):
    result = {}
    with open(fichier, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            result[key] = value
    return result


def chg_dico_json(fichier):
    with open(fichier, 'r') as f:
        return json.load(f)


def build_wiki_from(d, start_page):
    # print(len(d.keys()))
    if len(d.keys()) == 0:
        d.update({start_page: liste_liens(start_page)})
    for key in d.copy().keys():
        if d.copy()[key] is not None:
            for value in d.copy()[key]:
                if value not in d.keys():
                    d.update({value: liste_liens(value)})

    if not is_wiki_finished(d):
        build_wiki_from(d, start_page)
    return d


def build_wiki_from_largeur(wiki, source):
    f = []
    fait = []
    f.append(source)
    fait.append(source)
    while f:
        print(len(wiki.keys()))
        source = f.pop(0)
        wiki.update({source: liste_liens(source)})
        for voisin in wiki[source]:
            if voisin not in fait:
                f.append(voisin)
                fait.append(voisin)


def is_wiki_finished(dico):
    result = True
    for key in dico.copy().keys():
        if dico.copy()[key] is not None:
            for value in dico.copy()[key]:
                if value not in dico.keys():
                    result = False
    return result


# wiki = {}
# svg_dico_json(build_wiki_from_largeur(wiki, source), 'fichier_cible.json')

# les url Joffrey_I_Baratheon, Joffrey et Joffrey_Baratheon conduisent a la meme page, donc donnent la meme liste
# 2658 pages dans le dico contre 2534 pages dans le wiki, donc 124 urls conduisent a des pages identiques
# temps d'exec pour build le wiki depuis 'Petyr_Baelish': 5min7sec, 2658 pages
# temps d'exec pour build_largeur depuis 'Petyr_Baelish': 9min50sec, 2667 pages

def plus_court_chemin(page_source, page_cible):
    # result list
    result = []
    result.append(page_source)
    # wiki to search
    wiki = build_wiki_from({}, page_source)
    for key in wiki.keys():
        for value in wiki[key]:
            if value == page_cible:
                print(value)
                print(key)
                result.append(key)
                break
    result.append(page_cible)
    # RETURN
    if not result[1]:
        return None
    return result


source = 'Dorne'
cible = 'Rhaego'
print(plus_court_chemin(source, cible))
