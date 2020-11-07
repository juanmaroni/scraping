# Working with the CSV file and Pandas

import pandas as pd
import matplotlib.pyplot as plt
from scrap_heroes import csv_filepath

Df = pd.DataFrame

def analyze_heroes_from_csv():
    heroes_file: Df = pd.read_csv(csv_filepath, delimiter = '|', lineterminator = '\n', index_col='name')
    
    # Dropping columns I won't be using
    new_heroes_file: Df = heroes_file.drop(['portrait_pic_url', 'portrait_ingame_url', 'bio', 'lst_abilities'], axis = 1)

    # Printing top 5 rows from the dataset
    print('Top 5 rows:')
    print(new_heroes_file.head())
    print()

    # How many meelee and ranged heroes exist?
    total_melee: int = len(new_heroes_file[new_heroes_file['attack_type'] == 'Melee'])
    total_ranged: int = len(new_heroes_file[new_heroes_file['attack_type'] == 'Ranged'])

    print(f'Total melee Heroes: {total_melee}')
    print(f'Total ranged Heroes: {total_ranged}')
    print()

    print('Attack Type graph:')

    fig: plt = plt.figure()
    plt.title('Number of Heroes by Attack Type')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(['Melee', 'Ranged'], [total_melee, total_ranged])
    ax.get_children()[0].set_color('r')
    plt.show()

if __name__ == "__main__":
    analyze_heroes_from_csv()
