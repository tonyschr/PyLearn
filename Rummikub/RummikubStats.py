import RummikubSimulator as rs


def meld_statistics(trials, num_players, num_colors, duplicates_per_color, num_initial_tiles):
    rs.print_verbosity = 0
    meld_turn_total = 0
    meld_turn_count = 0
    never_melded = 0
    rummikub_count = 0

    for i in range(0, trials):
        rummikub = False
        rs.init_game(num_players, num_colors, duplicates_per_color, num_initial_tiles)

        while len(rs.stacked_tiles) > 0 and rummikub == False:
            for player in rs.players:
                player.play_turn()
                if len(player.tiles) == 0:
                    rummikub = True
                    rummikub_count = rummikub_count + 1
                    break
        
        for player in rs.players:
            if player.melded_turn > 0:
                meld_turn_count = meld_turn_count + 1
                meld_turn_total = meld_turn_total + player.melded_turn
            else:
                never_melded = never_melded + 1

    average_meld_turn = meld_turn_total / float(meld_turn_count)
    print(f"Games won: {rummikub_count / float(trials) * 100}%")
    print(f"Average turns before meld: {average_meld_turn}")
    print(f"Never melded: {never_melded / float(num_players * trials) * 100}%")



if __name__ == '__main__':
    meld_statistics(10, num_players = 2, num_colors = 4, duplicates_per_color = 2, num_initial_tiles = 14)
