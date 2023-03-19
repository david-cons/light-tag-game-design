from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from gamelogic import Player, Lobby

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

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
            lobby = Lobby([Player(form['username'], player_ip)])
            return redirect(url_for('lobby', lobby=lobby.id))
        
        else:

            #join
            if form['id'] not in Lobby.all_lobbies:

                return redirect('/')
            
            else:

                lobby = Lobby.all_lobbies[form['id']]

                if player_ip not in lobby.get_player_ips(): # might want to comment this line if you want to test locally
                    lobby.add_player(form['username'], player_ip)
                
                return redirect(url_for('lobby', lobby=lobby.id))
    else:

        return render_template('index.html', create_form = create_form, join_form = join_form)


@app.route('/<lobby>')
def lobby(lobby): #this has lobby id

    if lobby not in Lobby.all_lobbies or request.remote_addr not in Lobby.all_lobbies[lobby].get_player_ips(): # we do this second condition because people could enter the lobby by route alone

        return redirect('/')
    
    else:

        lobby = Lobby.all_lobbies[lobby]
        return render_template('lobby.html', lobby=lobby)
    

if __name__ == "__main__":
    app.run(debug=True)