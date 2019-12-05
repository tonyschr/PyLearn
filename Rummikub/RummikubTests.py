import re
import RummikubSimulator as rs

def parse_tile(tile_string):
    match = re.match(r"([)0-9]+)\[([a-z]+)\]", tile_string)
    return rs.Tile(match.group(1), rs.colors.index(match.group(2)))

def parse_tiles(tiles_string):
    tiles = []
    tile_string_list = tiles_string.split(' ')
    for tile_string in tile_string_list:
        tiles.append(parse_tile(tile_string))
    return tiles



#print(f"{tile.number} {tile.color}")



# board = [
#     [ Tile(4, 0), Tile(5, 0), Tile(6, 0), Tile(7, 0), Tile(8, 0), Tile(9, 0)],
# ]

# tile = Tile(7, 0)

# print_tile_sets("Before", board)
# try_add_to_run_on_board(tile)
# print_tile_sets("After", board)


# meld_statistics(num_players=4, num_colors=4, num_initial_tiles=14)

# for tile in stacked_tiles:
#     tile.print()

#test_tiles = [ Tile(1, 0), Tile(1, 0), Tile(2, 0), Tile(4, 0), Tile(5, 0), Tile(6, 0), Tile(1, 0), Tile(6, 0), Tile(7, 0), Tile(8, 0) ]

# test_tiles = [ Tile(1, 0), Tile(2, 0), Tile(3, 0), Tile(3, 0), Tile(4, 0)  ]

# test_tiles = [ Tile(5, 1), Tile(8, 1), Tile(9, 1), Tile(10, 1), Tile(11, 1), Tile(2, 2), Tile(4, 3) ]
#[black] 4[black] 9[black] 10[black] 1[blue] 2[blue] 4[blue] 5[blue] 8[blue] 9[blue] 10[blue] 11[blue] 2[red] 4[red] 7[red] 7[red] 8[red] 12[red] 2[orange] 6[orange] 8[orange] 8[orange] 9[orange] 11[orange] 13[orange]

# run = find_run(test_tiles)
# print_tiles("run", run)

# player = Player("Tony")
# player.tiles = test_tiles
# player.try_meld()

# for player in players:
#     player.print()
#     player.try_meld()

# print_tile_sets("Board after meld:", board)

