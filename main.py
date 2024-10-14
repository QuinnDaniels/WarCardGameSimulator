import requests
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

from api_modelsL4 import Deck, Pile, Card, jprint


#   Assistance from chatgpt
#   https://chatgpt.com/share/67043402-22f0-8010-aaae-cf2e5673f5a4


"""_summary_

    Returns:
        _type_: _description_
    """



class PlayState:
    def __init__(self, round_number=0, is_war=False, war_round=0, war_bounty=0):
        self.round_number = round_number
        self.is_war = is_war
        self.war_round = war_round
        self.war_bounty = war_bounty
    
    #def declare_war(self, new_state):
    #    """set a war_state to check if a war has been declared"""
    def __repr__(self):
        return f"Round: {self.round_number}.\n\tWar Active? : {self.is_war}\n\t\tWar Round: {self.war_round}"
        


# -----------------------------------------------------

"""
FUNCTIONS
"""


def card_value(card):
    """Convert a card value (2-10, JACK, QUEEN, KING, ACE) to a numeric value."""
    value = card['value']
    if value == 'JACK':
        return 11
    elif value == 'QUEEN':
        return 12
    elif value == 'KING':
        return 13
    elif value == 'ACE':
        return 14
    else:
        return int(value)  # Numeric cards (2-10)





def before_round(player1_pile, player2_pile):
    """QD - made to run before playing a round. Purpose is to change the obj_PlayState attributes and to check if a war is active

    Args:
        player1_pile (_type_): _description_
        player2_pile (_type_): _description_
    """
    
    # Increment the Round Number here to save on redundant code
    #obj_PlayState.round_number = obj_PlayState.round_number + 1
    
    # Check if a war is active. If so, play_war_round. Otherwise, play_round
    if obj_PlayState.is_war == True:
        play_war_round(player1_pile, player2_pile)
    else:
        play_round(player1_pile, player2_pile)




def play_round(player1_pile, player2_pile):
    # Draw one card for each player
    player1_card = player1_pile.draw_from_pile(1)[0]  # Draws one card and accesses the first card
    player2_card = player2_pile.draw_from_pile(1)[0]

    # Show the cards drawn
    print(f"Player 1 drew: {player1_card['value']} of {player1_card['suit']}")
    print(f"Player 2 drew: {player2_card['value']} of {player2_card['suit']}")

    # Compare the card values
    player1_value = card_value(player1_card)
    player2_value = card_value(player2_card)

    if player1_value > player2_value:
        print("Player 1 wins this round!")
        # Add both cards to Player 1's pile
        player1_pile.add_to_pile([player1_card, player2_card])
    elif player1_value < player2_value:
        print("Player 2 wins this round!")
        # Add both cards to Player 2's pile
        player2_pile.add_to_pile([player1_card, player2_card])
    else:
        print("It's a tie! Prepare for War!")
        #warpool_pile.add_to_pile([player1_card, player2_card])
        obj_PlayState.is_war = True
        #obj_PlayState.war_bounty = 2       #  set the initial value to 2 bc of cards in bounty


def play_war_round(player1_pile, player2_pile):
    """QD - redirects from _before_round()_ when a war is active. Redirects to _handle_war()_. Was originally made to create my own way of handling War's logic (which was not working, and I decided to give up) before I realized that ChatGPT generated a better (though different) way of handling War. This is the same reason why PlayState and _before_round()_ was created.

    
    """
    # increment war round
    handle_war(player1_pile, player2_pile)





def handle_war(player1_pile, player2_pile):
    """Handle a War scenario if both players draw the same card value."""
    print("War! Each player draws three more cards...")

    obj_PlayState.war_round = obj_PlayState.war_round + 1       #   QD - increment the war round
    
    
    # Each player draws 4 cards (3 facedown and 1 face-up for battle)
    player1_war_cards = player1_pile.draw_from_pile(4)
    player2_war_cards = player2_pile.draw_from_pile(4)

    # Compare the last card drawn (the face-up battle card)
    player1_war_card = player1_war_cards[-1]
    player2_war_card = player2_war_cards[-1]

    player1_value = card_value(player1_war_card)
    player2_value = card_value(player2_war_card)

    if player1_value > player2_value:
        print("Player 1 wins the war!")
        player1_pile.add_to_pile(player1_war_cards + player2_war_cards)
        
        obj_PlayState.is_war = False

    
    elif player1_value < player2_value:
        print("Player 2 wins the war!")
        player2_pile.add_to_pile(player1_war_cards + player2_war_cards)
    
        obj_PlayState.is_war = False
    
    else:
        print("Another tie during War! Could get interesting...")
        handle_war(player1_pile, player2_pile)  # Continue the War!
        










def play_game(player1_pile, player2_pile):
    """GPT - auto runs the game logic.
    Changed how the round number is tracked to tie it to the PlayState class I created earlie
    bc it felt odd to keep it tied to the method

    """
    obj_PlayState.round_number = 1 #obj_PlayState.war_round + 1     #   QD - sets initial round number in PlayState. changed from """roundNumber = 1"""
    
    
    while True:
        print(f"\n--- Round {obj_PlayState.round_number} ---")

        # Check if any player has run out of cards
        player1_cards = player1_pile.list_cards()
        player2_cards = player2_pile.list_cards()

        if len(player1_cards) == 0:
            print("Player 1 is out of cards! Player 2 wins the game!")
            break
        elif len(player2_cards) == 0:
            print("Player 2 is out of cards! Player 1 wins the game!")
            break

        # Play one round
        before_round(player1_pile, player2_pile)
        # p1_view(player1_pile)     # debug. Testing method
        
        obj_PlayState.round_number += 1  #round_number += 1





def active_play_game(player1_pile, player2_pile):
    """ QD - purpose is to be a way to step through the logic of war
    """
    obj_PlayState.round_number = 1 #obj_PlayState.war_round + 1     #   QD - sets initial round number in PlayState. changed from """roundNumber = 1"""
    
    
    player_choice = input("Press enter to begin")
    
    while True:
    

        # Check if any player has run out of cards
        player1_cards = player1_pile.list_cards()
        player2_cards = player2_pile.list_cards()

        if len(player1_cards) == 0:
            print("Player 1 is out of cards! Player 2 wins the game!")
            break
        elif len(player2_cards) == 0:
            print("Player 2 is out of cards! Player 1 wins the game!")
            break
        
        
        display_menu()
        
        # Play one round









def display_menu():
    while True:
        
        print(f"--- Round {obj_PlayState.round_number} ---")

        
        if obj_PlayState.is_war == True:
            print("\n1. WAR!!")
        elif obj_PlayState.is_war == False:
            print("\n1. Play Round!")
        print("2. View the current score")
        print("3. View the cards in Player1's Hand (DEBUG)")
        print("4. View the cards in Player2's Hand (DEBUG)")
        
        
        
        pchoice = input("Enter your choice: ")
        if pchoice == "1":      # Play one round
            print("...")
            before_round(player1_pile, player2_pile)
            obj_PlayState.round_number += 1  #round_number += 1
        if pchoice == "3":      # DEBUG - view p1 hand
            p1_view(player1_pile)
        if pchoice == "4":
            p2_view(player2_pile)
        if pchoice == "2":
            score_count(player1_pile, player2_pile)

                    






def score_count(player1_pile,player2_pile):
    p1c = len(player1_pile.list_cards())
    p2c = len(player2_pile.list_cards())
    print(f"Player 1 Score: {p1c}!")
    print(f"Player 2 Score: {p2c}!")
    
def p1_view(player1_pile):
    print(jprint(player1_pile.list_cards()))

def p2_view(player2_pile):
    print(jprint(player2_pile.list_cards()))


# --------------------------------------------------

# create a formatted string of the Python JSON object
#def jprint(obj):
#    text = json.dumps(obj, sort_keys=True, indent=4)
#    print(text)
#
#response = requests.get("https://deckofcardsapi.com/api/deck/new/")
#print(response.status_code)
#print(response.json())


# Brand New Deck
# https://deckofcardsapi.com/api/deck/new/


# New Deck + Shuffle the Cards:
# https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1


# SPLIT DECK (PART 1): Draw a Card:
# dividedDeck = 52 / NumOfPlayers
# "https://deckofcardsapi.com/api/deck/" + <<deck_id>> + "/draw/?count=" + dividedDeck



#Draw a Card (DECK):
#https://deckofcardsapi.com/api/deck/<<deck_id>>/draw/?count=




#jprint(response.json())


# Initialize the deck
deck = Deck()

obj_PlayState = PlayState(0, False)

# Each player will have a pile (hand of cards)
player1_pile = Pile(deck.deck_id, "player1")
player2_pile = Pile(deck.deck_id, "player2")
warpool_pile = Pile(deck.deck_id, "warpool")
bounty1_pile = Pile(deck.deck_id, "bounty1")
bounty2_pile = Pile(deck.deck_id, "bounty2")




# Draw cards for each player (e.g., 26 cards each, half the deck)
# Add the drawn cards to each player's pile
player1_cards = deck.draw_cards(26)
player2_cards = deck.draw_cards(26)
player1_pile.add_to_pile(player1_cards)
player2_pile.add_to_pile(player2_cards)



# Display cards for each player (for debugging purposes)
print("/n------------------------------------------/nPLAYER 1 START/n------------------------")
print("Player 1's hand:", player1_pile.list_cards())
print("/n------------------------------------------/nPLAYER 2 START/n------------------------")
print("Player 2's hand:", player2_pile.list_cards())


print("\n\n")

initloop = True
while initloop == True:
    print("Choose your style of play:")
    print("1. Auto Play Mode")
    print("2. Manual Play Mode")
    
    stylechoice = input("> ")

    if stylechoice == "1":
        play_game(player1_pile, player2_pile)
        initloop = False
    if stylechoice == "2":
        active_play_game(player1_pile, player2_pile)
        initloop = False
    else:
        print("\n\nSomething went wrong. Please try again")
        stylechoice == 0


print("Thank You for Playing!")

#print(f"\n\nplayer1:\n {jprint(player1_pile.list_cards())}")
#print(f"\n\nplayer2:\n {jprint(player2_pile.list_cards())}")


#-------------------------------------------------




