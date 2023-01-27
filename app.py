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
    l = []
    for link in soup:
        l.append(link.get('href'))
    print('len(l) with href ' + str(len(l)))
    # remove 'https://iceandfire.fandom.com'
    # for element in str(l):
    #     if 'https://iceandfire.fandom.com' in element:
    #         element.replace('https://iceandfire.fandom.com', '')
    # print('len(l) without https ' + str(len(l)))
    # remove elements from another website
    # for element in l:
    #     if 'https' in element:
    #         l.remove(element)
    # print('len(l) without foreign pages ' + str(len(l)))
    # remove elements with ':'
    print(l)
    l = [element for element in l if ':' in element]
    print('len(l) without ":" ' + str(len(l)))
    print(l)
    # remove '/wiki/'
    # for element in l:
    #     if '/wiki/' in element:
    #         element.replace('/wiki/', '')
    # print('len(l) without "/wiki/" ' + str(len(l)))
    # remove doubles
    # l = list(set(l))
    # print('len(l) without doubles ' + str(len(l)))
    # RETURN
    # if empty list, then there is no path, we must return None
    if (l == []): return None
    # else, return the list
    return l


# main('House_Lannister', 'House_Stark')
liste_liens('Petyr_Baelish')