

def update_points(result, match, tournament):
    for tournament_player in tournament.players_list:
        tp_player_id = tournament_player.player.chess_national_id
        m0_player_id = match[0].player.chess_national_id
        m1_player_id = match[1].player.chess_national_id
        if tp_player_id == m0_player_id:
            player1 = tournament_player
        if tp_player_id == m1_player_id:
            player2 = tournament_player
    if result == "draw":
        player1.tournament_points += 0.5
        player2.tournament_points += 0.5
    else:
        if result == player1.player.chess_national_id:
            player1.tournament_points += 1
        elif result == player2.player.chess_national_id:
            player2.tournament_points += 1


def have_played(p1, p2, match_history):
    pair = (p1.tournament_id, p2.tournament_id)
    reverse_pair = (p2.tournament_id, p1.tournament_id)
    return pair in match_history or reverse_pair in match_history
