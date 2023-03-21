from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_socketio import SocketIO, emit, join_room, leave_room
from wtforms import StringField, SubmitField
from threading import Thread
from gamelogic import Player, Lobby

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def index():

    class CreateForm(FlaskForm):
        username = StringField('username')
        submit = SubmitField('Create Game!')

    class JoinForm(FlaskForm):
        username = StringField('username')
        id = StringField('id')
        submit = SubmitField('Join Game!')

    create_form = CreateForm()
    join_form = JoinForm()
            

    if request.method == 'POST':

        form = request.form
        player_ip = request.remote_addr
        
        if 'id' not in form: # check if this is create or join.

            #create
            player_admin = Player(form['username'], player_ip, admin=True)

            lobby = Lobby([player_admin])

            return redirect(url_for('lobby', lobby=lobby.id, player= player_admin.id))
        
        else:

            #join
            if form['id'] not in Lobby.all_lobbies:

                return redirect('/')
            
            else:

                lobby = Lobby.all_lobbies[form['id']]

                new_player = Player(form['username'], player_ip)

                lobby.add_player(new_player)
                
                return redirect(url_for('lobby', lobby=lobby.id, player = new_player.id))
    else:

        return render_template('index.html', create_form = create_form, join_form = join_form)


@app.route('/<lobby>/<player>')
def lobby(lobby, player): #this has lobby id

    if lobby not in Lobby.all_lobbies or request.remote_addr not in Lobby.all_lobbies[lobby].get_player_ips(): # we do this second condition because people could enter the lobby by route alone

        return redirect('/')
    
    else:

        lobby = Lobby.all_lobbies[lobby]

        if len(lobby.players) == 1:
            thread = Thread(target=lobby.game, args=(socketio,10,10,None))
            thread.start()

        player = lobby.get_player_by_id(player)

        return render_template('lobby.html', lobby=lobby, player=player)
    
@socketio.on('connect')
def on_connect():
    print('A client connected')

@socketio.on('join')
def on_join(data):
    print('player: ' + data['player_id'] + ' from lobby: ' + data['lobby'] + ' is online and was assigned to socket room')
    
    join_room(data['lobby']) # we already know this has to exist

@socketio.on('disconnect')
def on_disconnect():
    pass # need to add code for leaving the room also


if __name__ == "__main__":
    socketio.run(app)