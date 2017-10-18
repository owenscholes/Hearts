import random

class Card:

    def __init__(self, val, su):
        self.suit = su
        self.value = val
        self.name = '%s of %s' % (self.value, self.suit)
        self.owner = None
        if type(self.value) == int:
            self.score = self.value
        elif self.value == 'Jack':
            self.score = 11
        elif self.value =='Queen':
            self.score = 12
        elif self.value == 'King':
            self.score = 13
        elif self.value == 'Ace':
            self.score = 14

    def printName(self):
        print '%s of %s' % (self.value, self.suit)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score

    def getName(self):
        return self.name
    def getSuit(self):
        return self.suit
    def setSuit(self, insuit):
        self.suit = insuit
    def getValue(self):
        return self.value
    def setValue(self, invalue):
        self.value = invalue
    def getOwner(self):
        return self.owner
    def setOwner(self, inp):
        self.owner = inp

class Deck:

    def __init__(self):
        self.valuePool = ['Ace','Jack','Queen','King']
        for x in range(2,11):
            self.valuePool.append(x)
        self.valuePool *= 4
        self.suitPool = ['Hearts', 'Diamonds', 'Spades', 'Clubs'] * 13
        self.library = []
        for x in range(52):
            self.library.append(Card(self.valuePool[x], self.suitPool[x]))

    def shuffle(self):
        random.shuffle(self.library)

    def getTopCard(self):
        return self.library.pop(0)

class Player:

    def __init__(self, iname):
        self.name = iname
        self.hand = []
        self.score = 0

    def drawCard(self, deck):
        self.hand.append(deck.getTopCard())
    def printHand(self):
        for i, x in enumerate(self.hand):
            print "%r:  %s" % (i, x.getName())

    def getHand(self):
        return self.hand
    def getName(self):
        return self.name
    def setName(self, inp):
        self.name = inp
    def getScore(self):
        return self.score
    def addScore(self, value):
        self.score += value


"Actual Game"
deck = Deck()
player1 = Player('A')
player2 = Player('B')
player3 = Player('C')
player4 = Player('D')
players = [player1,player2,player3,player4]

deck.shuffle()
deck.shuffle()
#Draw hands
for x in range(13):
    for player in players:
        player.drawCard(deck)
#Set ownership and assign lead
for p in players:
    for c in p.getHand():
        c.setOwner(p)
        if c.getName() == '2 of Clubs':
            lead = p
    p.getHand().sort()

for x in reversed(players):
    players.insert(0, players.pop(players.index(lead)))
    if x == lead:
        break

#Start of game
while player4.getHand() != [] and player3.getHand() != [] and player2.getHand() != [] and player1.getHand() != []:
    inPlay = []
    points = 0
    #Start of round
    for currentPlayer in players:
        print "\n----------------------------------------------------------------------------\n"
        print "It is %s's turn." % currentPlayer.getName()
        print "Cards in play:",
        for x in inPlay:
            print "%s, " % x.getName(),
        print
        print "To play a card, enter its index. To view your hand, type 'h'. To view scores, type 's'"

        if inPlay != []:
            leadsuit = inPlay[0].getSuit()
        else:
            leadsuit = None

        #Take player card choice input
        while True:
            legal = True
            choice = raw_input('> ')
            try:
                choice = int(choice)
            except ValueError:
                choice = str(choice)
            if type(choice) == int:
                if choice >= 0 and choice < len(currentPlayer.getHand()):
                    suits = []
                    for x in currentPlayer.getHand():
                        if x.getName() == '2 of Clubs' and choice != currentPlayer.getHand().index(x):
                            print "You must play the 2 of Clubs"
                            suits.append('two')
                        if x.getSuit() not in suits:
                            suits.append(x.getSuit())
                    if 'two' in suits:
                        legal = False

                    if currentPlayer.getHand()[choice].getSuit() != leadsuit and (leadsuit in suits) and (leadsuit != None):
                        print "You must play the suit that was led if you have it"
                        legal = False

                    if legal:
                        break
                else:
                    print "You don't have that many cards in your hand"
            elif choice == 'h':
                currentPlayer.printHand()
            elif choice == 's':
                for x in players:
                    print "%s: %d" % (x.getName(), x.getScore())
            else:
                print 'Command not recognized'
                print "To play a card, enter its index. To view your hand, type 'h'. To view scores, type 's'"
        #Plays the card
        inPlay.append(currentPlayer.getHand().pop(choice))


    #Count points in trick
    for x in inPlay:
        if x.getSuit() == 'Hearts':
            points += 1
        if x.getName() == "Queen of Spades":
            points += 13

    eligibleInPlay = []
    for x in inPlay:
        if x.getSuit() == leadsuit:
            eligibleInPlay.append(x)
    winner = max(eligibleInPlay).getOwner()
    winner.addScore(points)
    for x in reversed(players):
        players.insert(0, players.pop(players.index(winner)))
        if x == winner:
            break
    print "\n%s takes the trick for %d points" % (winner.getName(), points)


for x in players:
    print "%s: %d" % (x.getName(), x.getScore())
"""
TO DO
X   implement correct player order
X   Fix leadsuit checker
X   figure out trick win checker
X   2 of clubs
X   fix endgame condition with player order
"""


"Test zone"
"""dec = Deck()
dec.shuffle()
dec.shuffle()
dec.shuffle()
dec.shuffle()

me = Player()

for x in range(13):
    me.drawCard(dec)

me.printHand()



#for x in dec.library:
#    x.printName()
#print dec.suitPool
#print dec.valuePool
"""
