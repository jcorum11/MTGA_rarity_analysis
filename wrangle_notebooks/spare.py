import pandas as pd 
import numpy as np

decks_clean = pd.read_csv('C:/Users/muroc/Documents/MTG/data/decks_clean.csv')

card_lists = []
for index, rows in decks_clean.iterrows():
    li = [rows.deck_list]
    card_lists.append(li)

cards = []
for li in card_lists:
    for a in li: 
        cards.append(card)

print(cards)