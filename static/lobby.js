let socket = null;
let my_player_id = null;
let my_lobby_id = null;


window.onload = function() {
    my_player_id = document.getElementById('player-id').innerHTML;
    my_lobby_id = document.getElementById('lobby-id').innerHTML;

    socket = io.connect('http://' + document.domain + ':' + location.port);
    join();

    socket.on('update_lobby', function(data) {
        console.log(data['players']);
        display_players(data['players']);
        
        my_color = null;
        for(const [id, color] of Object.entries(data['players']))
        {
            if(id == my_player_id)
            {
                my_color = color;
            }
        }

        change_background_color(my_color);
    });

    document.addEventListener('click', function(){
        console.log(my_player_id + ' is time-outed');
        socket.emit('time-out', {'lobby' : my_lobby_id, 'player_id' : my_player_id, });
    });
}

window.onbeforeunload = function () {
    socket.emit('leave', {'lobby' : my_lobby_id , 'player_id' : my_player_id} );
}

function join()
{
    socket.emit('join', {'lobby' : my_lobby_id, 'player_id': my_player_id});
}

function display_players(players) 
{
    let ul = document.createElement('ul');
    ul.id = 'list';

    for(const [id, color] of Object.entries(players))
    {
        let li = document.createElement('li');
        li.textContent = id + ' ' + (color === null? 'time-outed' : color);

        ul.appendChild(li);
    }
    
    let player_container = document.getElementById('players');
    existing_list = document.getElementById('list');

    if (existing_list !== null)
        player_container.removeChild(document.getElementById('list'));

    player_container.appendChild(ul);
}

function change_background_color(color)
{
    document.body.style.backgroundColor = color === null ? 'yellow' : color;
}