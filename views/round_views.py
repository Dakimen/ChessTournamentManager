def display_round_history(rounds):
    for round in rounds:
        print(round.name)
        for match in round.matches:
            print(f"{match[0].player.surname} {match[0].player.name}, "
                  f"{match[0].player.chess_national_id} "
                  f"pts: {match[0].tournament_points} "
                  "vs "
                  f"{match[1].player.surname} {match[1].player.name}, "
                  f"{match[1].player.chess_national_id} "
                  f"pts: {match[1].tournament_points}")
