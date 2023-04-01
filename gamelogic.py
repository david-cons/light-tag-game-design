from random import randint, sample
import threading
import time
import gevent
from flask import copy_current_request_context
from flask_socketio import SocketIO# in the game loop we need to send messages to the players

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

    def game(self, socketio, start_game_wait_time, time_out_time, game_mode = None): #timing is done in seconds
        print(str(self.id) + ' game is running')
        gevent.sleep(start_game_wait_time) # start of the game time until everybody is ready
        #print the amount of time people have to get ready for 
        lap = 0
        while True: #game_loop
            lap += 1
            #print everybody's colors 

            if len(self.players) == 0:
                print(str(self.id) + ' game is closed')
                return # end thread when there are no more players in the game
        
            if lap == 1 or game_mode == 'dynamic':
                print("switching players colors in lobby: " + str(self.id) + " at lap: " + str(lap))
                self.switch_players_colors()

            self.send_current_lobby_state(socketio=socketio)

            gevent.sleep(time_out_time)

            
    def switch_players_colors(self):
        # we want about 33% of players to be taggers
        # we want about 66% of players to be runners
        # we want to make sure there is at least 1 tagger always

        shuffled_list = sample(self.players, len(self.players))
        tagger = 'red'
        runner = 'blue'

        for (k,i) in enumerate(shuffled_list):
            if k % 3 == 0:
                self.get_player_by_id(i.id).color = tagger
            else:
                self.get_player_by_id(i.id).color = runner

        
    def send_current_lobby_state(self,socketio):
           everybody = {}

           for i in self.players:
               everybody[i.id] = i.color

           socketio.emit('update_lobby', {'players' : everybody}, to=self.id)



class Player:

    def __init__(self, name, ip):

        self.name = name
        
        self.ip = ip

        self.id = self.name + '-' + str(randint(0, 1000))

        self.sid = None #socket session ID must be actualized when user gets connected via socket

        self.color = None #Timeouted
    