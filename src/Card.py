# Name: Anish Jain
# AndrewID: anishjai
# Section K
# @version: 12.6.24

from cmu_graphics import *
from random import *
import os

def getImagePath(filename):
    """Get the correct path for image files from the images folder"""
    # Get the directory where this file is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'images', filename)

# The card class represents a singular card in the deck. Number 1, 11, 12, and 13 represent 
# Ace, Jack, Queen, and King respectively. The suits are represented by 0 (hearts), 
# 1 (diamonds), 2 (clubs), and 3 (spades). 
# Images for suits are from : https://cdn.vectorstock.com/i/1000v/54/38/playing-card-suits-vector-23605438.jpg
# back_card.jpg was designed using canva and the following 2 images:
# https://www.cmu.edu/brand/brand-guidelines/images/seal-4c-600x600-min.jpg
# https://www.cmu.edu/brand/brand-guidelines/images/lettermark-600x600.jpg

class Card:
   # Dictionary containing suit name and associated png image
   suits = {
    'H': "Hearts.png",
    "D": "Diamonds.png",
    "C": "Clubs.png",
    "S": "Spades.png"
   }

   # Constructor for Card class. Rotangle and isHidden are used for drawing the card on display.
   def __init__(self, suitNum, value, rotangle, isHidden):
      self.suitNum = suitNum
      self.value = value
      self.rotangle = rotangle
      self.suit = Card.numToSuitName(self.suitNum)
      # self.suitEmoji = Card.getEmoji(self.suitNum)
      self.valueDepiction = Card.valueDepiction(self.value)
      self.isHidden = isHidden
   
   def __repr__(self):
      return self.valueDepiction + self.suit
   
   # Tells if two cards are equal
   def __eq__(self, other):
      return (isinstance(other, Card) and self.suitNum == other.suitNum and 
              self.value == other.value)
   
   def __hash__(self):
      return hash(str(self))

   def flipCard(self):
      self.isHidden = not self.isHidden
      return self

   # draws the card at a certain location
   def depict(self, xCoor, yCoor, width=100, height=150, rotAngle=0):
      if self.isHidden:
         drawImage(getImagePath('back_card.jpg'), xCoor, yCoor, width=width, height=height)
         drawRect(xCoor, yCoor, width, height, fill=None, border='black', borderWidth=2)
      else:
         img = getImagePath(self.suits[self.suit])
         drawRect(xCoor, yCoor, width, height, fill='white', border='black', borderWidth=2)
         suitColor = rgb(200,70,59) if self.suitNum<=1 else 'black'
         drawRect(xCoor + 10, yCoor + 10, width - 20, height - 20, fill=None, border=suitColor, borderWidth=1)

         squareSize = 25  # Size of the white squares
         drawRect(xCoor + 5, yCoor + 5, squareSize, squareSize, fill='white')  # Top-left square
         drawRect(xCoor + width - squareSize - 5, yCoor + height - squareSize - 5, squareSize, squareSize, fill='white')  # Bottom-right square
        
         drawLabel(self.valueDepiction, xCoor + 8, yCoor + 12, size=20, fill=suitColor, align='left', font='cursive')
         drawImage(img, xCoor + width / 4, yCoor + height / 3, width=width / 2, height=height/3)
         # drawLabel(self.suit, xCoor + width / 2, yCoor + height / 2, size=20, fill='black', align='center')
         drawLabel(self.valueDepiction, xCoor + width - 5, yCoor + height - 15, size=20, fill=suitColor, align='right', font='cursive')



   # Gives name of the suit based on the associated number. The suits are represented
   # by 0 (hearts), # 1 (diamonds), 2 (clubs), and 3 (spades).

   @staticmethod
   def numToSuitName(num):
      if num == 0: return 'H'
      if num == 1: return 'D'
      if num == 2: return 'C'
      return 'S'
   
   # @staticmethod
   # def getEmoji(num):
   #    return Card.suits[Card.numToSuitName(num)]
   
   @staticmethod
   def valueDepiction(num):
      if 2 <= num <= 10:
         return str(num)
      if num == 1 or num == 14: return 'A'
      if num == 11: return 'J'
      if num == 12: return 'Q'
      return 'K'
   
   @staticmethod
   def getRandomCard():
      return Card(random.randint(0, 3), random.randint(1,13), 0)

   # def drawCard(self):

      