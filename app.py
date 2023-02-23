from pip._vendor import requests
from bs4 import BeautifulSoup
import json

BASE = 'https://iceandfire.fandom.com/wiki/'


def main(source, cible):
    """doc main"""
    print('source: ', source)
    print('cible: ', cible)


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


def svg_dico(dico, file):
    with open(file, 'w') as f:
        for key, value in dico.items():
            f.write(f'{key}: {value}\n')


def svg_dico_json(dico, file):
    with open(file, 'w') as f:
        json_str = json.dumps(dico, indent=4)
        f.write(json_str)


def chg_dico(file):
    result = {}
    with open(file, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            result[key] = value
    return result


def chg_dico_json(file):
    with open(file, 'r') as f:
        return json.load(f)


def build_wiki_from(dico, source):
    print(len(dico.keys()))
    if len(dico.keys()) == 0:
        dico.update({source: liste_liens(source)})
    for key in dico.copy().keys():
        if dico.copy()[key] is not None:
            for value in dico.copy()[key]:
                if value not in dico.keys():
                    dico.update({value: liste_liens(value)})

    if not is_wiki_finished(dico):
        build_wiki_from(dico, source)
    return dico


def build_wiki_from_largeur(wiki, source):
    f = []
    done = []
    f.append(source)
    done.append(source)
    while f:
        print(len(wiki.keys()))
        source = f.pop(0)
        wiki.update({source: liste_liens(source)})
        for voisin in wiki[source]:
            if voisin not in done:
                f.append(voisin)
                done.append(voisin)


def is_wiki_finished(wiki):
    result = True
    for key in wiki.copy().keys():
        if wiki.copy()[key] is not None:
            for value in wiki.copy()[key]:
                if value not in wiki.keys():
                    result = False
    return result


# wiki = {}
# svg_dico_json(build_wiki_from_largeur(wiki, source), 'fichier_cible.json')

# les url Joffrey_I_Baratheon, Joffrey et Joffrey_Baratheon conduisent a la meme page, donc donnent la meme liste
# 2658 pages dans le dico contre 2534 pages dans le wiki, donc 124 urls conduisent a des pages identiques
# temps d'exec pour build le wiki depuis 'Petyr_Baelish': 5min7sec, 2658 pages
# temps d'exec pour build_largeur depuis 'Petyr_Baelish': 9min50sec, 2667 pages

def plus_court_chemin(source, cible):
    # wiki to search
    wiki = chg_dico_json('wiki.json')
    # result list
    result = []
    found = False
    result.append(source)
    # go through wiki from source and not from the start
    for key in wiki[source]:
        for value in wiki[key]:
            if value == cible:
                result.append(key)
                result.append(value)
                found = True
            if found:
                break
        if found:
            break
    if not found:
        pass
    # RETURN
    if not found:
        print('no path found')
        return None
    return result


# wiki = {}
# wiki = build_wiki_from(wiki, 'Petyr_Baelish')
# svg_dico_json(wiki, 'wiki.json')

source = 'Dorne'
cible = 'Rhaego'
cible2 = 'Nymeria'
cible3 = 'Arya_Stark'
cible4 = 'Needle'
print(plus_court_chemin(source, cible3))
# ['Dorne', 'House_Targaryen', Rhaego']
# ['Dorne', 'Rhoynar', 'Nymeria', 'Arya_Stark', 'Needle']
