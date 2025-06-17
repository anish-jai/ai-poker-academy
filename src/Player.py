# Name: Anish Jain
# AndrewID: anishjai
# Section K
# @version: 12.6.24

from cmu_graphics import *
from Card import *
import Deck
import random 

# The Player class represents a player, that can either be an AI or the user itself. It contains methods that calculates
# probabilities using monte carlo methods
class Player:
   def __init__(self, name, amount, aiType):
      self.name = name
      self.cards = []
      self.isFolded = False
      self.amount = amount
      self.aiType = aiType

   def assignHand(self, inhand):
      self.cards = inhand

   def simulateOutcomes(self, flop, numberOfOutcomes):
      randDeck = Deck.Deck()
      randDeck.shuffleDeck()
      outcomes = [0] * 9
      for i in range(numberOfOutcomes):
         adjustedFlop = set(flop)
         randDeck.resetDeck()
         while(len(adjustedFlop) < 5):
            tempCard = randDeck.dealCard()
            if tempCard not in self.cards and tempCard not in adjustedFlop:
               adjustedFlop.add(tempCard)
         curFlop = list(adjustedFlop)
         curHand = Player.chooseBestHand(self.cards, curFlop)
         # print(curFlop, curHand, Player.assignRankingToHand(curHand))
         outcomes[Player.assignRankingToHand(curHand)] += 1
         # print(' ')
      return [outcomes[i]/numberOfOutcomes for i in range(len(outcomes))]

   def fold(self):
      self.isFolded = True
   
   def bet(self, betAmount):
      self.amount -= betAmount
   
   # tells how good a players hand is, scaled based on the probabilities of their monte carlo simulation
   def calculateBetability(self, flop):
      currentFlop = []
      cardsOut = 0
      for c in flop:
         if not c.isHidden:
            currentFlop.append(c)
            cardsOut += 1

      weightedChance = 0
      # For each type of hand, weights array contains average chance of winning given that hand
      weights = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 1]
      currentProbabilities = self.simulateOutcomes(currentFlop, 3000)
      for i in range(len(weights)):
         weightedChance += weights[i] * currentProbabilities[i]
      return weightedChance, cardsOut


   # AI bet is based on the riskiness of the cpu and amount of money currently held
   def makeAIBet(self, betAmount, flop):
      betability, cardsOut = self.calculateBetability(flop)
      betThreshold = 0
      if self.aiType == 'Scared':
         betThreshold = 0.35  + betAmount/self.amount
      elif self.aiType == 'Neutral':
         betThreshold = 0.28 + 0.5 * betAmount/self.amount
      elif self.aiType == 'Risky':
         betThreshold = 0.25  + 0.25 * betAmount/self.amount
      else:  # AI is just random
         random_number = random.randint(1, 100)
         if random_number > betAmount:
            return betAmount
         else:
            return -1
      
      # print(f'The betability for {self.name} is {betability} and the threshold is {betThreshold}')
      if betability >= betThreshold * 1.5:
         if self.aiType == 'Scared':
            return int((betAmount * (random.uniform(1.5, 3.0)) + self.amount * 0.05 * (betability/betThreshold - 1)))
         elif self.aiType == 'Neutral':
            return int((betAmount * (random.uniform(1.5, 4.0)) + self.amount * 0.1 * (betability/betThreshold - 1)))
         elif self.aiType == 'Risky':
            return int((betAmount * (random.uniform(2.0, 5.0)) + self.amount * 0.2 * (betability/betThreshold - 1)))
         return int(betAmount * (1.5 * betability/betThreshold))
      elif betability >= betThreshold:
         return betAmount
      else:
         return -1
      
   # Gives best hand out of all possible combinations of hand and flop
   @staticmethod
   def chooseBestHand(hand, flop):
      bestHand = None
      # bestRanking = 0   # referes to high card; assume high card is initially best
      for i in range(len(flop)):
         for j in range(i+1, len(flop)):
            for k in range(j+1, len(flop)):
               curHand = hand + [flop[i], flop[j], flop[k]]
               bestHand = Player.betterHand(bestHand, curHand)
      # print(hand)
      # print("choosebesthand method", bestHand)
      return bestHand


   @staticmethod
   def betterHand(hand1, hand2):
      if hand1 == None: return hand2
      rankH1 = Player.assignRankingToHand(hand1)
      rankH2 = Player.assignRankingToHand(hand2)
      if rankH1 > rankH2: return hand1
      if rankH2 > rankH1: return hand2
      numsOne = sorted(Player.numsOnly(hand1))
      numsTwo = sorted(Player.numsOnly(hand2))
      for i in range(len(numsOne)-1, 0, -1):
         if numsOne[i] > numsTwo[i]: return hand1
         if numsTwo[i] > numsOne[i]: return hand2
      return hand1


   # Assigning ranking helps compare hands. "Rankings" are as follows, based on Texas Hold'em hands:
   # 0: High Card
   # 1: Pair
   # 2: Two Pair
   # 3: Three of A Kind
   # 4: Straight
   # 5: Flush
   # 6: Full House
   # 7: Four of A Kind
   # 8: Straight Flush
   @staticmethod
   def assignRankingToHand(hand):
      if Player.hasStraightFlush(hand): return 8
      if Player.hasFourOfAKind(hand): return 7
      if Player.hasFullHouse(hand): return 6
      if Player.hasFlush(hand): return 5
      if Player.hasStraight(hand): return 4
      if Player.hasThreeOfAKind(hand): return 3
      if Player.hasTwoPair(hand): return 2
      if Player.hasPair(hand): return 1
      return 0

   @staticmethod
   def numsOnly(hand):
      return [hand[i].value for i in range(len(hand))]

   @staticmethod
   def suitsOnly(hand):
      return [hand[i].suitNum for i in range(len(hand))] 

   @staticmethod 
   def hasPair(hand):
      numHand = Player.numsOnly(hand)
      return len(numHand) - len(set(numHand)) > 0
   
   @staticmethod 
   def hasTwoPair(hand):
      numHand = Player.numsOnly(hand)
      pairCounts = [numHand.count(val) for val in set(numHand)]
      numPairs = pairCounts.count(2)
      return numPairs == 2

   @staticmethod 
   def hasThreeOfAKind(hand):
      numHand = Player.numsOnly(hand)
      uniqueNums = set(numHand)
      for val in uniqueNums:
         if(numHand.count(val) > 2): return True
      return False
   
   @staticmethod
   def hasStraight(hand):
      numHand = Player.numsOnly(hand)
      numHand.sort()
      for i in range(len(numHand)-1):
         if numHand[i] + 1 != numHand[i+1]:
            return False
      return True
   
   @staticmethod
   def hasFlush(hand):
      suitHand = Player.suitsOnly(hand)
      return len(set(suitHand)) == 1
   
   @staticmethod
   def hasFullHouse(hand):
      numHand = Player.numsOnly(hand)
      numHand.sort()
      return len(set(numHand)) == 2 and numHand.count(numHand[0]) >= 2 and numHand.count(numHand[-1]) >= 2
   
   @staticmethod 
   def hasFourOfAKind(hand):
      numHand = Player.numsOnly(hand)
      uniqueNums = set(numHand)
      return len(set(numHand[1:])) == 1 or len(set(numHand[:-1])) == 1
   
   @staticmethod
   def hasStraightFlush(hand):
      return Player.hasFlush(hand) and Player.hasStraight(hand)




