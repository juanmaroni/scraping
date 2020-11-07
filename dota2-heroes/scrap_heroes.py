# Source: http://www.dota2.com/heroes/
# Scrap some data from the source and put it on a CSV file

import os
from typing import List
import requests
from bs4 import BeautifulSoup
import csv
import time

Response = requests.models.Response

# Using os.path to get complete filepath and set CSV name
# Making it accessible for other modules to work with the data
csv_filepath: str = f'{os.path.dirname(__file__)}/data_heroes.csv'

def scrap_heroes_to_csv():
    # I could create a list with the links/names of the heroes to form their URLs
    # but I will get them by scraping, so I don't have to update if Valve adds
    # a new hero (Soon TM)
    all_heroes_url: str = 'http://www.dota2.com/heroes/'
    resp: Response = requests.get(all_heroes_url)

    if resp.status_code == 200:
        hero_links: List = []
        bs: BeautifulSoup = BeautifulSoup(resp.text, 'html.parser')
        bs_hero_links: BeautifulSoup = bs.findAll('a', class_='heroPickerIconLink')

        for hl in bs_hero_links:
            hero_links.append(hl['href'])
        
        # Column names in the CSV
        field_names: List = ['name', 'portrait_pic_url', 'attack_type', 'lst_roles', 'portrait_ingame_url', 'intelligence',
            'int_gain', 'agility', 'agi_gain', 'strength', 'str_gain', 'min_base_damage', 'max_base_damage', 'base_speed',
            'armor', 'day_vision', 'night_vision', 'bio', 'lst_abilities']

        f = open(csv_filepath, 'w')
        f.write('|'.join(field_names) + '\n')
        
        for hero in hero_links:
            resp = requests.get(hero)
            
            if resp.status_code == 200:
                bs = BeautifulSoup(resp.text, 'html.parser')
                hero_page: BeautifulSoup = bs.find('div', id='centerColContent')
                
                # Hero name
                name: str = hero_page.find('h1').text

                # Portrait picture URL
                portrait_pic_url: str = hero_page.find('img', id='heroTopPortraitIMG')['src']
                
                # Attack type (range or meelee) and roles
                attackType_and_roles: List = hero_page.find('p', id='heroBioRoles').text.split(' - ')
                attack_type: str = attackType_and_roles[0]
                lst_roles: str = ', '.join(attackType_and_roles[1:])
                
                # In-game portrait URL
                portrait_ingame_url: str = hero_page.find('img', id='heroPrimaryPortraitImg')['src']
                
                # Main stats
                int_values: List = hero_page.find('div', id='overview_IntVal').text.split(' + ')
                intelligence: str = int_values[0]
                int_gain: str = int_values[1]
                agi_values: List = hero_page.find('div', id='overview_AgiVal').text.split(' + ')
                agility: str = agi_values[0]
                agi_gain: str = agi_values[1]
                str_values: List = hero_page.find('div', id='overview_StrVal').text.split(' + ')
                strength: str = str_values[0]
                str_gain: str = str_values[1]
                
                # Base damage
                damage: List = hero_page.find('div', id='overview_AttackVal').text.split(' - ')
                min_base_damage: str = damage[0]
                max_base_damage: str = damage[1]
                
                # Base speed
                base_speed: str = hero_page.find('div', id='overview_SpeedVal').text
                
                # Armor
                armor: str = hero_page.find('div', id='overview_DefenseVal').text
                
                # Vision range
                vision: List = hero_page.find('div', id='statsRight').find('div', class_='statRowCol2W').text.split(' / ')
                day_vision: str = vision[0]
                night_vision: str = vision[1]
                
                # Biography
                bio: str = hero_page.find('div', id='bioInner').text.strip()
                
                # Abilities
                bs_abilities: BeautifulSoup = hero_page.findAll('div', class_='overviewAbilityRowDescription')
                lst_abilities: List = []

                for ab in bs_abilities:
                    lst_abilities.append(ab.h2.text)

                abilities: str = ', '.join(lst_abilities)

                fields_data: List = [name, portrait_pic_url, attack_type, lst_roles, portrait_ingame_url, intelligence,
                    int_gain, agility, agi_gain, strength, str_gain, min_base_damage, max_base_damage, base_speed,
                    armor, day_vision, night_vision, bio, abilities]

                f.write('|'.join(fields_data) + '\n')
                
                # Don't abuse, pause between heroes
                # It will take more time, but it helps to prevent being blocked
                time.sleep(1)
        
        f.close()
    else:
        exit()

if __name__ == "__main__":
    scrap_heroes_to_csv()
