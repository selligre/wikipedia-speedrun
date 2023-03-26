import sys
from pip._vendor import requests
from bs4 import BeautifulSoup
import json
import math

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


def plus_court_chemin(source, cible):
    wiki = chg_dico_json('wiki.json')
    parents = build_parents_from(source, wiki)
    if cible not in parents:
        return None
    chemin = plus_court_chemin_rec(source, cible, parents)
    return chemin


def plus_court_chemin_rec(source, cible, parents):
    if source == cible:
        return [source]
    chemin = plus_court_chemin_rec(source, parents[cible], parents)
    chemin.append(cible)
    return chemin


def build_parents_from(source, wiki):
    parents = {}
    queue = [source]
    explored = [source]
    while queue:
        page = queue.pop(0)
        for link in wiki[page]:
            if link not in explored:
                parents[link] = page
                queue.append(link)
                explored.append(link)
    return parents


def nombre_caracteres(cible):
    return len(cible)


def nombre_voyelle(cible):
    count = 0
    for char in cible:
        if char in ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U', 'y', 'Y']:
            count += 1
    return count


def cout(cible):
    return nombre_caracteres(cible) + 2 * nombre_voyelle(cible)


# wiki = {}
# wiki = build_wiki_from(wiki, 'Petyr_Baelish')
# svg_dico_json(wiki, 'wiki.json')
source = 'Dorne'
cible = 'Waif'
# ['Dorne', 'House_Targaryen', 'Barristan_Selmy', 'Arya_Stark', 'Waif']
cible2 = 'Aurion'
# no path to 'Aurion'
print(plus_court_chemin(source, cible))
