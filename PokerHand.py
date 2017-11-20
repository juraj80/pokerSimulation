from Card import Card,Hand, Deck


class PokerHand(Hand):
    """Represents a poker hand."""

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.
        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
##        print(self.suits)

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def rank_hist(self):
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank]=self.ranks.get(card.rank,0) + 1

    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise.
        Note that this works correctly for hands with more than 5 cards.
        """
        self.rank_hist()
        for val in self.ranks.values():
            if val == 2:
                return True
        return False
    
    def has_twopair(self):
        self.rank_hist()
        count = 0
        for val in self.ranks.values():
            if val == 2:
                count += 1
                
        if count == 2:
            return True
        else:
            return False

    def has_threeofkind(self):
        self.rank_hist()
        for val in self.ranks.values():
            if val == 3:
                return True
        return False

    def has_straight(self):
        self.rank_hist()
        ranks = sorted(list(self.ranks.keys()))
##        print(ranks)        
        count = 0
        i = 1
        while i<len(ranks):
            diff = ranks[i]-ranks[i-1]
            if diff == 1:
                count += 1
                if count == 4:
                    return True
            else:                 
                count = 0
            i += 1
        return False

    def has_fullhouse(self):
        self.rank_hist()
##        print(self.ranks)
        if 3 in self.ranks.values() and 2 in self.ranks.values():
            return True
        return False

    def has_fourofkind(self):
        self.rank_hist()
##        print(self.ranks)
        if 4 in self.ranks.values():
            return True
        return False

    def has_straightflush(self):
        self.rank_hist()
        self.suit_hist()
        newhand = []
        for key, value in self.suits.items():
            if value >= 5:
                for card in self.cards:
                    if card.suit == key:
                        newhand.append(card.rank)
        if newhand != []:
            newhand.sort()
            count = 0
            i = 1
            while i < len(newhand):
                diff = newhand[i] - newhand[i-1]
                if diff == 1:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
                i += 1
            return False
        else:
            return False

    def classify(self):
    
        if self.has_straightflush():
            self.label = 'straightflush'          
        elif self.has_fourofkind():
            self.label = 'fourofkind'
        elif self.has_fullhouse():
            self.label = 'fullhouse'
        elif self.has_straight():
            self.label = 'straight'
        elif self.has_threeofkind():
            self.label = 'threeofkind'
        elif self.has_twopair():
            self.label = 'twopair'
        elif self.has_pair():
            self.label = 'pair'
        else:
            self.label = 'nopair'

def game(handSize,players):
    deck = Deck()
    deck.shuffle()
    hand_labels = []
    for i in range(players):
        hand = PokerHand()
        deck.move_cards(hand,handSize)
        hand.sort()
        hand.classify()
        hand_labels.append(hand.label)
    label_dict = dict()     
    for label in hand_labels:
        label_dict[label]=label_dict.get(label,0) + 1
    return (label_dict)

def probability(card,hand,players):
    for key,value in hand.items():
        if key == card:
            return value/players
    return 0

def frequency(num_games,handSize,players):
    frequencies = {'nopair':0,'pair':0,'twopair':0,'threeofkind':0,'straight':0,'fullhouse':0,'fourofkind':0, 'straightflush':0}
    for i in range(num_games):
        if i % 1000 == 0:
            print(i,sep='',end=' ',flush=True)
        labels = game(handSize,players)
        for key,value in labels.items():
            frequencies[key] += value
    return frequencies
    
def simulation(num_games,handSize,players):
    frequencies = frequency(num_games,handSize,players)
    result = {}       
    for key, value in frequencies.items():
        result[key] = round(value/num_games/players*100,2)
##    print(frequencies)
    print('\n')
    print('The probabilities of each type of {}-card hand:'.format(handSize))
    return result
        
    
               
if __name__ == '__main__':
    num_games = 10000
    handSize = 7
    players = 7
    print('Compare my result to the values at https://en.wikipedia.org/wiki/Poker_probability')
    print('\n')
    print('Running simulation for {} games with {} players.'.format(num_games,players))
    print('\n')
    print('No. of games:')
    print(simulation(num_games,handSize,players))
    
    
