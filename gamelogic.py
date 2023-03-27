from random import randint
import threading
import time
from server import send_current_lobby_state

class Lobby:
    
    all_lobbies = {}

    def __init__(self,  players = None):
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
    
    def get_player_ids(self):

        return map(lambda x: x.id, self.players)
    
    def add_player(self, player):

        self.players.append(player)

    def get_player_by_id(self, player_id):
        result = [i for i in self.players if i.id == player_id]

        if len(result) == 0:

            return None
        
        return result[0]
    
    def remove_player(self, player):
        self.players.remove(player)

    def game(self, start_game_wait_time, time_out_time,game_mode = None): #timing is done in seconds
        
        time.sleep(start_game_wait_time) # start of the game time until everybody is ready
        #print the amount of time people have to get ready for 

        while True: #game_loop
            #print everybody's colors 

            if len(self.players) == 0:
                return # end thread when there are no more players in the game
        
            for i in self.players:
                i.color = 'blue' if randint(0,1) == 1 else 'red'

            send_current_lobby_state(self)

            time.sleep(time_out_time)


class Player:

    def __init__(self, name, ip):

        self.name = name
        
        self.ip = ip

        self.id = self.name + '-' + str(randint(0, 1000))

        self.sid = None #socket session ID must be actualized when user gets connected via socket

        self.color = None #Timeouted
    