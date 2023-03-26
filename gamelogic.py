from random import randint
import threading
import time

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

    def game(self, socketio, start_game_wait_time, time_out_time ,game_mode = None): #timing is done in seconds

        socketio.sleep(start_game_wait_time) # start of the game time until everybody is ready
        #print the amount of time people have to get ready for 

        while True: #game_loop
            #print everybody's colors 

            for i in self.players:
                i.color = 'blue' if randint(0,1) == 1 else 'red'

            self.send_current_lobby_state(socketio=socketio)

            socketio.sleep(time_out_time)

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
    