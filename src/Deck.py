# Name: Anish Jain
# AndrewID: anishjai
# Section K
# @version: 12.6.24

from cmu_graphics import *
from Card import *
from Player import *
import random

# The Deck class represents a standard deck of 52 cards using the Card class.
class Deck:
   def __init__(self):
      self.cards = Deck.unshuffledDeck()

   # Gives a deck, with all cards in order
   @staticmethod
   def unshuffledDeck():
      return [Card(suit, value, 0, True) for suit in range(4) for value in range(1, 14)]
   
   def shuffleDeck(self):
      random.shuffle(self.cards)

   def resetDeck(self):
      self.cards = Deck.unshuffledDeck()
      self.shuffleDeck()
   
   def deckRemains(self):
      return True if len(self.cards) > 0 else False

   def dealCard(self):
      if self.deckRemains():
         return self.cards.pop()
      return None
   
   def dealHand(self, size, Player):
      hand = [self.dealCard() for i in range(size)]
      Player.cards = hand
      return hand
   
   def dealFlop(self):
      flop = [self.dealCard() for i in range(5)]
      return flop
   
   def insertCard(self, insertCard):
      self.cards.append(insertCard)