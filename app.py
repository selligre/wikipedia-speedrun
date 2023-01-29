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
    # remove 'https://iceandfire.fandom.com'
    for element in range(len(liste)):
        if 'https://iceandfire.fandom.com' in liste[element]:
            liste[element] = liste[element].replace('https://iceandfire.fandom.com', '')
    # remove elements from another website
    for element in range(len(liste) - 1):
        if 'https' in liste[len(liste) - element - 1]:
            liste.pop(element)
    # remove elements with 'Local_Sitemap'
    for element in range(len(liste) - 1):
        if 'Local_Sitemap' in liste[len(liste) - element - 1]:
            liste.pop(element)
    # remove elements with ':' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if ':' not in element]
    # remove elements with 'POV' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if 'POV' not in element]
    # remove elements with '=' REFAIRE AVEC LA BOUCLE POP
    liste = [element for element in liste if '=' not in element]
    # remove elements with 'community'
    liste = [element for element in liste if 'community' not in element]
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
print(liste_liens('Petyr_Baelish'))
