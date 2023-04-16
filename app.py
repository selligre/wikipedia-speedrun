from bs4 import BeautifulSoup
import json
import math
import requests

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'


# QUESTION 1:
def liste_liens(page):
    content = requests.get(WIKI_URL + page)
    soup = BeautifulSoup(content.content, 'html.parser')
    soup = soup.select('div.mw-parser-output a[href^="/wiki/"][title]')
    liste = []
    for link in soup:
        liste.append(link.attrs['href'][len('/wiki/'):])
    # remove elements with impurities
    liste = [element for element in liste if ':' not in element]
    # remove doubles
    liste = list(set(liste))
    # RETURN
    return liste


# QUESTION 1: test
# print('---------- QUESTION 1: test ----------')
# print(liste_liens('Petyr_Baelish'))


# QUESTION 2:
def svg_dico(dico, file):
    with open(file, 'w') as f:
        json_str = json.dumps(dico, indent=4)
        f.write(json_str)


# QUESTION 2: test
# print('---------- QUESTION 2: test ----------')
# svg_dico(liste_liens('Petyr_Baelish'), 'question2.json')


# QUESTION 3
def chg_dico(file):
    with open(file, 'r') as f:
        return json.load(f)


# QUESTION 3: test
# print('---------- QUESTION 3: test ----------')
# print(chg_dico('question2.json'))


# QUESTION 4:
def build_wiki(wiki, source):
    f = []
    done = []
    f.append(source)
    done.append(source)
    while f:
        source = f.pop(0)
        # wiki.update({source: liste_liens(source)})
        wiki[source] = liste_liens(source)
        for voisin in wiki[source]:
            if voisin not in done:
                f.append(voisin)
                done.append(voisin)
    return wiki


# QUESTION 4: test
# print('---------- QUESTION 4: test ----------')
svg_dico(build_wiki({}, 'Petyr_Baelish'), 'wiki.json')


# print(chg_dico('wiki.json'))


# QUESTION 5:
def plus_court_chemin(source, cible, wiki):
    parents = build_parents(source, cible, wiki)
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


def build_parents(source, cible, wiki):
    parents = {}
    queue = [source]
    explored = [source]
    while queue:
        page = queue.pop(0)
        if page == cible:
            return parents
        for link in wiki[page]:
            if link not in explored:
                parents[link] = page
                queue.append(link)
                explored.append(link)
    return parents


# QUESTION 5: test
# print('---------- QUESTION 5: test ----------')
# print("test de l'enonce : ")
# print(plus_court_chemin('Dorne', 'Rhaego', chg_dico('wiki.json')))
# print("test plus complexe : ")
# print(plus_court_chemin('Dorne', 'Waif', chg_dico('wiki.json')))
# print("test pour pas de chemin : ")
# print(plus_court_chemin('Dorne', 'Aurion', chg_dico('wiki.json')))


# QUESTION 6:
def pcc_voyelles(source, cible):
    parents = dijkstra(chg_dico('wiki.json'), cout, source, cible)
    if source == cible:
        return [source]
    if cible not in parents:
        return None
    chemin = plus_court_chemin_rec(source, parents[cible], parents)
    chemin.append(cible)
    return chemin


def dijkstra(wiki, cout, source, cible):
    distance = {}
    parents = {}

    def initialisation(wiki, source):
        for s in wiki:
            distance[s] = math.inf
        distance[source] = 0

    def trouve_min(queue):
        mini = math.inf
        sommet = -1
        for item in queue:
            if distance[item] < mini:
                mini = distance[item]
                sommet = item
        return sommet

    def maj_distances(sommet_1, sommet_2):
        if distance[sommet_2] > distance[sommet_1] + cout(sommet_2):
            distance[sommet_2] = distance[sommet_1] + cout(sommet_2)
            parents[sommet_2] = sommet_1

    initialisation(wiki, source)
    queue = list(wiki.keys())
    while queue:
        sommet_1 = trouve_min(queue)
        if sommet_1 == cible:
            return parents
        queue.remove(sommet_1)
        for sommet_2 in wiki[sommet_1]:
            maj_distances(sommet_1, sommet_2)
    return parents


def cout(cible):
    def nombre_caracteres(cible):
        return len(cible)

    def nombre_voyelles(cible):
        count = 0
        for char in cible:
            if char in ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U', 'y', 'Y']:
                count += 1
        return count

    return nombre_caracteres(cible) + nombre_voyelles(cible)


# QUESTION 6: test
# print('---------- QUESTION 6: test ----------')
# print("test de l'enonce : ")
# print(pcc_voyelles('Dorne', 'Rhaego'))
# print("test plus complexe : ")
# print(pcc_voyelles('Dorne', 'Waif'))
# print("test pour pas de chemin : ")
# print(pcc_voyelles('Dorne', 'Aurion'))


# QUESTION 7:
def characters():
    base_url = "https://iceandfire.fandom.com/wiki/"
    url = "https://iceandfire.fandom.com/wiki/Category:Characters"
    char_list = {}
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for character in soup.find('div', attrs={'class': 'category-page__members'}).find_all('a'):
            name = character.attrs['title']
            siblings = []
            parents = []
            children = []
            lovers = []
            page1 = requests.get(base_url + character.attrs['href'][6:])
            soup1 = BeautifulSoup(page1.content, "html.parser")
            for relation in soup1.find_all("div", {"class": "pi-item pi-data pi-item-spacing pi-border-color"}):
                relation_type = relation.find("h3").get_text()
                for item in relation.find_all("a"):
                    relation_name = item.get_text()
                    if relation_type == "Siblings":
                        siblings.append(relation_name)
                    elif relation_type == "Father":
                        parents.append(relation_name)
                    elif relation_type == "Mother":
                        parents.append(relation_name)
                    elif relation_type == "Children":
                        children.append(relation_name)
                    elif relation_type == "Lover":
                        lovers.append(relation_name)
                    elif relation_type == "Spouse":
                        lovers.append(relation_name)
            char_list[name] = {"siblings": siblings, "parents": parents, "children": children, "lovers": lovers}
        nextPage = soup.find('a', attrs={'class': 'category-page__pagination-next wds-button wds-is-secondary'})
        if nextPage is None:
            return char_list
        url = nextPage.get('href')


# QUESTION 7: test
# print('---------- QUESTION 7: test ----------')
svg_dico(characters(), 'characters.json')


# print(chg_dico('characters.json'))


# QUESTION 8:
def find_incest():
    liste = chg_dico('characters.json')
    incest = []
    for char in liste:
        for lov in liste[char]['lovers']:
            if ((char, lov) not in incest) and ((lov, char) not in incest):
                if lov in liste[char]['siblings'] or lov in liste[char]['parents'] or lov in liste[char]['children']:
                    incest.append((char, lov))
    return incest


# QUESTION 8: test
# print('---------- QUESTION 8: test ----------')
# print(find_incest())


# QUESTION 9:
def descendances():
    liste = chg_dico('characters_corrected.json')
    descendances = {}

    def descendances_rec(char):
        if char in descendances:
            return descendances[char]
        if not liste[char]['children']:
            return []
        result = []
        for child in liste[char]['children']:
            descendances[child] = descendances_rec(child)
            result += [child] + descendances[child]
        return result

    for char in liste:
        if char not in descendances:
            descendances[char] = descendances_rec(char)

    return descendances


# QUESTION 9: test
# print('---------- QUESTION 9: test ----------')
svg_dico(descendances(), 'famille.json')
# print(chg_dico('famille.json'))
