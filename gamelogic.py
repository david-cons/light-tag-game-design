from random import randint

class Lobby:
    
    all_lobbies = {}

    def __init__(self, players = None):
        trial = str(randint(0,1000))
        while trial in Lobby.all_lobbies:
            trial = str(randint(0,1000))

        self.id = trial

        if players == None:
            self.players = []
        else:
            self.players = players

        Lobby.all_lobbies[trial] = self

    def get_id(self):

        return self.id
    
    def get_player_ips(self):

        return map(lambda x: x.ip, self.players)
    
    def add_player(self, player):

        self.players.append(player)

    def get_player(self, player_id):
        result = [i for i in self.players if i.id == player_id]

        if len(result) == 0:

            return None
        
        return result[0]

class Player:

    def __init__(self, name, ip, admin=False, colors=None):

        self.name = name
        
        self.ip = ip

        self.id = self.name + '-' + str(randint(0, 1000))

        if colors == None:

            self.colors = ['Red', 'Blue']

        else: 

            self.colors = colors

        self.color = None #Timeouted
    