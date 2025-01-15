import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

# A classe Service é usada para iniciar uma instância do Chrome WebDriver
service = Service()
# webdriver.ChromeOptions é usado para definir a prefêrencia para o browser do Chrome.
options = webdriver.ChromeOptions()
# Inicia a instância do Chrome Webdriver com as definidas 'options' e 'service'
driver = webdriver.Chrome(service=service, options=options)
listaurls = []  # depois usar o append
ocorrenciaspokemon = dict()
tipos_pokemon = [
    "Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water",
    "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"
]
# Lista combinada de todos os itens
itens_filtro = [
    "Cheri Berry", "Chesto Berry", "Pecha Berry", "Rawst Berry", "Aspear Berry", "Leppa Berry", "Oran Berry", 
    "Persim Berry", "Lum Berry", "Kebia Berry", "Shuca Berry", "Colbur Berry", "Babiri Berry", "Chople Berry", 
    "Tanga Berry", "Kasib Berry", "Haban Berry", "Colbur Berry", "Babiri Berry", "Rindo Berry", "Wacan Berry", 
    "Yache Berry", "Passho Berry", "Rindo Berry", "Wacan Berry", "Yache Berry", "Macho Berry", "Sitrus Berry",
    "Payapa Berry",
    
    "Energy Powder", "Energy Root", "Heal Powder", "Revival Herb",
    
    "Leftovers", "Choice Band", "Choice Specs", "Choice Scarf", "Assault Vest", "Focus Sash", "Focus Band", 
    "Black Sludge", "Life Orb", "White Herb", "Mental Herb", "Luminous Moss", "Razor Claw", "Razor Fang", 
    "Sharp Beak", "Black Belt", "Magnet", "Twisted Spoon", "Sea Incense", "Silk Scarf", "Wide Lens", "Zoom Lens", 
    "Amulet Coin", "Exp Share", "Eject Button", "Eviolite", "Red Card", "Quick Claw", "Smooth Rock", "Damp Rock", 
    "Heat Rock", "Light Clay", "Icy Rock", "Sticky Barb", "Black Glasses", "Spell Tag", "Toxic Orb", "Flame Orb", 
    "Grip Claw", "Focus Sash", "Eject Button", "Soft Sand",
    
    "Normalium Z", "Fightingium Z", "Flyingium Z", "Poisonium Z", "Groundium Z", "Rockium Z", "Buginium Z", 
    "Ghostium Z", "Steelium Z", "Fireium Z", "Waterium Z", "Grassium Z", "Electrium Z", "Psychium Z", "Icium Z", 
    "Dragonium Z", "Darkinium Z", "Fairium Z", "Fairium Z", "Kommonium Z", "Fightinium Z", "Firium Z", "Flyinium Z",
    
    "Medichamite", "Gyaradosite", "Venusaurite", "Charizardite X", "Charizardite Y", "Blazikenite", "Lopunnite", 
    "Alakazite", "Mawilite", "Mawileite", "Aerodactylite", "Beedrillite", "Sableyeite", "Manectite", "Lucarionite", 
    "Scizorite", "Pinsirite", "Garchompite", "Heracronite", "Lopunnyite", "Tyranitarite", "Cameruptite", "Diancite", 
    "Salamencite", "Mawilite", "Lunatite", "Pidgeotite"
]


def vefocorrencias(poke_names):
    for pokemon in poke_names:
        if pokemon in ocorrenciaspokemon:
            ocorrenciaspokemon[pokemon] += 1
        else:
            ocorrenciaspokemon[pokemon] = 1

def pegatime(url):
    driver.get(url)
    driver.implicitly_wait(5)
    source_code = driver.page_source
    soup = BeautifulSoup(source_code, "html.parser")
    
    poke_names = []  # Limpa a lista para cada nova URL
    for pre in soup.find_all("pre"):
        spans = pre.find_all("span", class_=lambda x: x and x.startswith("type-"))
        for span in spans:
            pokemon_name = span.text.strip()
            if pokemon_name != "-" and pokemon_name not in tipos_pokemon and pokemon_name not in itens_filtro:
                poke_names.append(pokemon_name)
    
    vefocorrencias(poke_names)

tier = None
url = None
href = None
print("Bem-Vindo ao analisador de ocorrência de pokémons em tier da smogon.\nUtilize o site com o template dos times do TIER atual da smogon e o programa analisará os pokémons.")
print("Responda as Perguntas:\n")
while True:
    tier = input("Digita o Tier = ")
    url = input("Digita a URL = ")
    if url and tier:
        break
    else:
        print("Erro: Ambos os campos são obrigatórios. Tente novamente.\n")

if not url.startswith("http://") and not url.startswith("https://"):
    print("Erro: A URL deve começar com 'http://' ou 'https://'.")
else:
    print(f"Tier informado: {tier}")
    print(f"URL informada: {url}")
    driver.get(url)

source_code = driver.page_source
soup = BeautifulSoup(source_code, "html.parser")
for link in soup.find_all("a", href=True):
    href = link["href"]
    if href.startswith("https://pokepast.es/"):
        listaurls.append(href)

for link in listaurls:
    pegatime(link)

# Organiza o dicionário por ocorrências em ordem decrescente
ocorrencias_sorted = sorted(ocorrenciaspokemon.items(), key=lambda x: x[1], reverse=True)

# Exibe o resultado
for item, ocorrencia in ocorrencias_sorted:
    print(f"{item}: {ocorrencia}")