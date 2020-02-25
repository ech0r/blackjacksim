from random import shuffle
#import tensorflow as tf
import re
import random
import sqlite3
import numpy as np


class Shoe:
    # A shoe object
    # size is number of decks. e.g. six decks in a shoe.
    def __init__(self, size):
        self.cards = []
        for k in range(size):
            for x in range(2,11):
                self.cards.append("%dH" % x)
                self.cards.append("%dS" % x)
                self.cards.append("%dC" % x)
                self.cards.append("%dD" % x)
            other = ["K","Q","J","A"]
            for face in other:
                self.cards.append("%sH" % face)
                self.cards.append("%sS" % face)
                self.cards.append("%sC" % face)
                self.cards.append("%sD" % face)

    def shuffle(self):
        shuffle(self.cards)


class Player:
    def __init__(self, style, bankroll):
        self.record = 0
        self.style = style
        self.bankroll = bankroll
        self.hand = []
        self.score = 0
        self.acecount = 0
        self.bet = 0

    def basicstrat(self,dealercard):
        move = ''
        # hard 11 or less
        if self.score <= 11 and self.acecount ==0:
                move = 'hit'
        # hard 12 against dealer 4-6
        if self.score == 12 and self.acecount == 1:
            nums = [4, 5, 6]
            # check if dealer card is a 4-6
            if any(num in dealercard for num in nums):
                move = 'stand'
            else:
                move = 'hit'
        # hard 13-16 against dealer 2-6
        if self.score >= 13 and self.score <= 16 and self.acecount == 1:
            nums = ['2', '3', '4', '5', '6']
            if any(num in dealercard for num in nums):
                move = 'stand'
            else:
                move = 'hit'
        # player has hard 17 or greater
        if self.score >= 17:
            if self.acecount == 0:
                move = 'stand'
        # player has a soft 17 or less
        if self.score <= 17:
            if self.acecount == 1:
                move = 'hit'
        # player soft 18
        if self.score == 18:
            if self.acecount == 1:
                nums = ['9', '10', 'J', 'Q', 'K', 'A']
                if any(num in dealercard for num in nums):
                    move = 'hit'
                else:
                    move = 'stand'
        # player soft 19
        if self.score >= 19:
            if self.acecount == 1:
                move = 'stand'
        return move

    def action(self, playedcards, dealercard):
        # randomly get true or false
        # every player will play randomly until I can get basic strategy worked out
        self.total()
        self.bet = 10
        move = ''
        count = 0

        # if player is a random
        if self.style == 'random':
            if self.score < 21:
                if bool(random.getrandbits(1)):
                    move = 'hit'
                else:
                    move = 'stand'
            else:
                move = 'stand'
            self.bet = 10*random.randint(1, 11)
        # if player is a counter
        if self.style == 'counter':
            # do card counting stuff
            highnums = ['2', '3', '4', '5', '6']
            lownums = ['10', 'J', 'Q', 'K', 'A']

            for card in playedcards:
                if any(highnum in card for highnum in highnums):
                    count += 1
                if any(lownum in card for lownum in lownums):
                    count -= 1
            move = self.basicstrat(dealercard)
            truecount = int(round(count/(len(playedcards)/52)))
            # bet spread dependent on count
            self.bet = truecount * 10

        # if player just uses basic strategy
        if self.style == 'basic':
            move = self.basicstrat(dealercard)
        return move



    def clearhand(self):
        self.hand = []
        self.acecount = 0

    def total(self):
        self.score = 0
        self.acecount = 0
        for card in self.hand:
            if "A" in card:
                self.score += 11
                self.acecount += 1
            elif "K" in card:
                self.score += 10
            elif "Q" in card:
                self.score += 10
            elif "J" in card:
                self.score += 10
            elif "10" in card:
                self.score += 10
            elif "9" in card:
                self.score += 9
            elif "8" in card:
                self.score += 8
            elif "7" in card:
                self.score += 7
            elif "6" in card:
                self.score += 6
            elif "5" in card:
                self.score += 5
            elif "4" in card:
                self.score += 4
            elif "3" in card:
                self.score += 3
            else:
                self.score += 2
        # modify score based on number of aces in hand
        while self.score > 21 and self.acecount > 0:
            # we need to modify the total.
            self.score = self.score - 10
            self.acecount -= 1

    def record(self, result):
        # if player won
        if (result == 1):
            self.record += 1
        else:
            self.record -= 1


class Dealer:
    def __init__(self):
        self.hand = []
        self.score = 0

    def total(self):
        self.score = 0
        acecount = 0
        for card in self.hand:
            if "A" in card:
                self.score += 11
                acecount += 1
            elif "K" in card:
                self.score += 10
            elif "Q" in card:
                self.score += 10
            elif "J" in card:
                self.score += 10
            elif "10" in card:
                self.score += 10
            elif "9" in card:
                self.score += 9
            elif "8" in card:
                self.score += 8
            elif "7" in card:
                self.score += 7
            elif "6" in card:
                self.score += 6
            elif "5" in card:
                self.score += 5
            elif "4" in card:
                self.score += 4
            elif "3" in card:
                self.score += 3
            else:
                self.score += 2
        # modify score based on number of aces in hand
        while self.score > 21 and acecount > 0:
            # we need to modify the total.
            self.score = self.score - 10
            acecount -= 1

    def action(self):
        self.total()
        if self.score < 17:
            return 'hit'
        else:
            return 'stand'

    def clearhand(self):
        self.hand = []


class Game:
    def __init__(self, numberofdecks,numberofplayers,playertype):
        names = ["Alex", "Janet", "Steve", "Chao", "Chang", "Yeti", "Nina", "Jess", "Matt", "Brad", "Chad"]
        self.deck = Shoe(numberofdecks)
        self.deck.shuffle()
        self.dealer = Dealer()
        self.players = {}
        self.playedcards = []
        for x in range(numberofplayers):
            name = random.randint(0,10)
            bankroll = 10000
            #TODO: change this
            self.players['Alex'] = Player(playertype, bankroll)

    def initialdeal(self):
        # deals two cards to each player and dealer
        for x in range(2):
            for player in self.players.values():
                player.hand += self.deck.cards[0]
                self.playedcards.append(self.deck.cards[0])
                del self.deck.cards[0]
            self.dealer.hand += self.deck.cards[0]
            self.playedcards.append(self.deck.cards[0])
            del self.deck.cards[0]

    def moves(self):
        for player in self.players.values():
            while True:
                action = player.action(self.playedcards, self.dealer.hand[0])
                if action == 'hit':
                    if player.score < 21:
                        player.hand += self.deck.cards[0]
                        self.playedcards.append(self.deck.cards[0])
                        del self.deck.cards[0]
                        player.total()
                else:
                    break
        while True:
            action = self.dealer.action()
            if action == 'hit':
                self.dealer.hand += self.deck.cards[0]
                self.playedcards.append(self.deck.cards[0])
                del self.deck.cards[0]
                self.dealer.total()
            else:
                break

    def tallyscore(self):
        winners = {}
        losers = {}
        tiedplayers = {}
        self.dealer.total()
        for name, player in self.players.items():
            player.total()
            # dealer gets blackjack
            if self.dealer.score == 21:
                if player.score == 21:
                    tiedplayers[name] = player
                else:
                    losers[name] = player
                    player.bankroll -= player.bet
            # dealer busts
            if self.dealer.score > 21:
                if player.score <= 21:
                    winners[name] = player
                    player.bankroll += player.bet
                else:
                    losers[name] = player
                    player.bankroll -= player.bet
            # dealer gets less than 21
            if self.dealer.score < 21:
                if player.score > self.dealer.score:
                    if player.score <= 21:
                        winners[name] = player
                        player.bankroll += player.bet
                    else:
                        losers[name] = player
                        player.bankroll -= player.bet
                else:
                    losers[name] = player
                    player.bankroll -= player.bet

        return winners, tiedplayers, losers
        #print("The following players beat the dealer:\n")
        #print("Dealer Score: ", self.dealer.score)
        #print("These players won: ", winnerscores)
        #print("These players tied: ", tiedplayers)
        #print("These players lost: ", loserscores)

    def bankrolltotals(self):
        bankrolls = {}
        for name, player in self.players.items():
            bankrolls[name] = player.bankroll
        return bankrolls


    def endround(self):
        self.dealer.clearhand()
        for player in self.players.values():
            player.clearhand()

    def endsession(self):
        self.playedcards = []
        self.deck = Shoe(6)
        self.deck.shuffle()