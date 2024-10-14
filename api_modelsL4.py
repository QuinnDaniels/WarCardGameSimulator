from pydantic import BaseModel



#   Assistance from ChatGPT
#   https://chatgpt.com/share/67043402-22f0-8010-aaae-cf2e5673f5a4


#class Deck(BaseModel)
#    deck_id    : str
#    remaining  : int
#    shuffled   : str
#    success    : str
    
    

import requests
import json


# create a formatted string of the Python JSON object
def jprint(obj):
    """ GPT - create a formatted string of the Python JSON object

    Args:
        obj (_type_): json object
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



class Deck:
    def __init__(self):
        self.deck_id = None
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck and gets a new deck_id"""
        response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/')
        data = response.json()
        self.deck_id = data['deck_id']
        print(f"Deck shuffled. Deck ID: {self.deck_id}")

    def draw_cards(self, count=1):
        """Draw a specific number of cards from the deck"""
        url = f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={count}"
        response = requests.get(url)
        data = response.json()
        return data['cards']  # This returns a list of card objects



class Card:
    def __init__(self, value, suit, code, image, images):
        self.value = value
        self.suit = suit
        self.code = code
        self.image = image
        self.images = images

    def __repr__(self):
        return f"{self.value} of {self.suit} - {self.code}"




class Pile:
    def __init__(self, deck_id, pile_name):
        self.deck_id = deck_id
        self.pile_name = pile_name

    def add_to_pile(self, cards):
        """Add cards to the pile"""
        card_codes = ','.join([card['code'] for card in cards])
        url = f"https://deckofcardsapi.com/api/deck/{self.deck_id}/pile/{self.pile_name}/add/?cards={card_codes}"
        response = requests.get(url)
        return response.json()

    def draw_from_pile(self, count=1):
        """Draw cards from the pile"""
        url = f"https://deckofcardsapi.com/api/deck/{self.deck_id}/pile/{self.pile_name}/draw/?count={count}"
        response = requests.get(url)
        return response.json()['cards']  # Returns a list of drawn cards

    def list_cards(self):
        """List the cards in the pile"""
        url = f"https://deckofcardsapi.com/api/deck/{self.deck_id}/pile/{self.pile_name}/list"
        response = requests.get(url)
        return response.json()['piles'][self.pile_name]['cards']
