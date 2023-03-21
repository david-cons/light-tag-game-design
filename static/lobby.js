let socket = null;
let my_player_id = null;
let my_lobby_id = null;

let my_players_color = null;

socket = null

window.onload = function() {

    my_player_id = document.getElementById('player-id').innerHTML;
    my_lobby_id = document.getElementById('lobby-id').innerHTML;

    socket = io.connect('http://' + document.domain + ':' + location.port);
    join()
    
    socket.on('event', function(data) {
        console.log(data)
    });
}

function join()
{
    socket.emit('join', {'lobby' : my_lobby_id, 'player_id': my_player_id});
}

