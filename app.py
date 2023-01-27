from pip._vendor import requests

print("start")

base = "https://iceandfire.fandom.com/wiki/"
source = ""
cible = ""


def main(source, cible):
    print("source: ", source)
    print("cible: ", cible)

def liste_liens(page):
    print(requests.get(base + page))

main("House_Lannister", "House_Stark")
liste_liens("House_Lannister")
