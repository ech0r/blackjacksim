from blackjack import *
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

sqlconnection = sqlite3.connect('blackjackdata.db')
cur = sqlconnection.cursor()
winnerslist = []
tieslist = []
loserslist = []
bankrolldata = []
game = Game(8, 1, 'counter')
for k in range(100):
    for j in range(12):
        for i in range(30):
            game.initialdeal()
            game.moves()
            winners, ties, losers = game.tallyscore()
            bankrolldata.append(game.players['Alex'].bankroll)
            if winners:
                winnerslist.append(winners)
            if ties:
                tieslist.append(ties)
            if losers:
                loserslist.append(losers)
            game.endround()
        game.endsession()

print("\n\nBankroll Totals: ", game.bankrolltotals())
print("Number of wins: ", len(winnerslist))
print("Number of ties: ", len(tieslist))
print("Number of losses: ", len(loserslist))
#plot bankroll over time
plt.plot(bankrolldata)
plt.title('Bankroll over time, random strategy, random betting (1 session)')
plt.ylabel('Dollars')
plt.xlabel('Hands Played')
plt.show()