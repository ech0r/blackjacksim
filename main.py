from blackjack import *
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

sqlconnection = sqlite3.connect('blackjackdata.db')
cur = sqlconnection.cursor()
winnerslist = []
tieslist = []
loserslist = []
bankrolldatarandom = []
bankrolldatabasic = []
bankrolldatacounter = []
gamer = Game(8, 1, 'random')
for k in range(100):
    for j in range(12):
        for i in range(30):
            gamer.initialdeal()
            gamer.moves()
            winners, ties, losers = gamer.tallyscore()
            bankrolldatarandom.append(gamer.players['Alex'].bankroll)
            if winners:
                winnerslist.append(winners)
            if ties:
                tieslist.append(ties)
            if losers:
                loserslist.append(losers)
            gamer.endround()
        gamer.endsession()

gameb = Game(8, 1, 'basic')
for k in range(100):
    for j in range(12):
        for i in range(30):
            gameb.initialdeal()
            gameb.moves()
            winners, ties, losers = gameb.tallyscore()
            bankrolldatabasic.append(gameb.players['Alex'].bankroll)
            if winners:
                winnerslist.append(winners)
            if ties:
                tieslist.append(ties)
            if losers:
                loserslist.append(losers)
            gameb.endround()
        gameb.endsession()

gamec = Game(8, 1, 'counter')
for k in range(100):
    for j in range(12):
        for i in range(30):
            gamec.initialdeal()
            gamec.moves()
            winners, ties, losers = gamec.tallyscore()
            bankrolldatacounter.append(gamec.players['Alex'].bankroll)
            if winners:
                winnerslist.append(winners)
            if ties:
                tieslist.append(ties)
            if losers:
                loserslist.append(losers)
            gamec.endround()
        gamec.endsession()

#plot bankroll over time
plt.plot(bankrolldatarandom)
plt.title('Bankroll over time, random strategy, random betting (100 sessions)')
plt.ylabel('Dollars')
plt.xlabel('Hands Played')
plt.show()

#plot bankroll over time
plt.plot(bankrolldatabasic)
plt.title('Bankroll over time, basic strategy, minimum betting (100 sessions)')
plt.ylabel('Dollars')
plt.xlabel('Hands Played')
plt.show()

#plot bankroll over time
plt.plot(bankrolldatacounter)
plt.title('Bankroll over time, basic strategy, with bet spread (100 sessions)')
plt.ylabel('Dollars')
plt.xlabel('Hands Played')
plt.show()