# CODE SNIPPETS



"""
def play_war_round(player1_pile, player2_pile):
    # increment war round
    obj_PlayState.war_round = obj_PlayState.war_round + 1
    

"""

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
    print("Player 1 wins the war!")
    # Add both cards to Player 1's pile
    player1_pile.add_to_pile([player1_card, player2_card])

    while obj_PlayState.war_bounty > 0: # Add the cards in warpool to Player 1's pile
        bounty_cards = warpool_pile.draw_from_pile(2)[0] # Draws one card and accesses the first card
        player1_pile.add_to_pile(bounty_cards)
        obj_PlayState.war_bounty -= 2
        
    # Change obj_PlayState attributes
    
    obj_PlayState.is_war = False
    obj_PlayState.war_round = 0

    
elif player1_value < player2_value:
    print("Player 2 wins the war!")
    # Add both cards to Player 2's pile
    player2_pile.add_to_pile([player1_card, player2_card])

    while obj_PlayState.war_bounty > 0:   # Add the cards in warpool to Player 2's pile
        bounty_cards = warpool_pile.draw_from_pile(2)[0] # Draws one card and accesses the first card
        player2_pile.add_to_pile(bounty_cards)
        obj_PlayState.war_bounty -= 2
        
    # Change obj_PlayState attributes
    obj_PlayState.is_war = False
    obj_PlayState.war_round = 0


else:
    print("It's a tie! Prepare for War!")
    warpool_pile.add_to_pile([player1_card, player2_card])
    obj_PlayState.war_bounty = obj_PlayState.war_bounty + 2
