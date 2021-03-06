import random

# TODO
#   - Harvest tiles
#   - More academic and/or Python conventions?
#       - Remove globals
#       - Make more functional style, e.g. returning board with new sets instead of 
#         modifying existing board. Or, return sets to add/remove.
#   - Find and rank multiple solutions
#       - Order of play (runs vs. groups)
#       - Combined with harvesting tiles
#       - Getting rid of high numbered tiles first

max_tile_number = 13
colors = ["black", "blue", "red", "orange", "pink", "purple", "green", "gold", "silver", "white"]

stacked_tiles = []
board = []
players = []
print_verbosity = 10

def print_tiles(prefix, tiles):
    if print_verbosity == 0:
        return
    tiles.sort()
    print(prefix, end=" ")
    for tile in tiles:
        tile.print()
    print("")


def print_tile_sets(prefix, tile_sets):
    if print_verbosity == 0:
        return
    print(prefix)
    for tile_set in tile_sets:
        print_tiles("    ", tile_set)


def remove_tiles(tiles, tiles_to_remove):
    for tile in tiles_to_remove:
        try:
            tiles.remove(tile)
        except ValueError:
            pass


def number_of_tile(tile):
    """Used to sort by number, irrespective of color"""
    return tile.number


def find_harvestable_tiles():
    """Returns full list of harvestable tiles, though the caller should only harvest one at a time"""
    harvestable_tiles = []
    for tile_set in board:
        if len(tile_set) > 3:
            harvestable_tiles.append(tile_set[0])
            harvestable_tiles.append(tile_set[len(tile_set) - 1])
    return harvestable_tiles


def find_run(tiles):
    """Returns the first run of at least 3 tiles."""
    tiles.sort()
    current_run = []

    for i in range(len(tiles)):
        if len(current_run) == 0:
            current_run.append(tiles[i])
        else:
            if tiles[i].color == current_run[len(current_run) - 1].color:
                if tiles[i].number == current_run[len(current_run) - 1].number:
                    continue
                elif tiles[i].number == current_run[len(current_run) - 1].number + 1:
                    current_run.append(tiles[i])
                else:
                    if len(current_run) >= 3:
                        return current_run

                    # TODO: Consolidate with below else?
                    current_run.clear()
                    current_run.append(tiles[i])
            else:
                if len(current_run) >= 3:
                    return current_run

                current_run.clear()
                current_run.append(tiles[i])

    if len(current_run) >= 3:
        return current_run

    return []


def find_group(tiles):
    tiles.sort(key=number_of_tile)
    current_group = []

    for i in range(len(tiles)):
        if len(current_group) == 0:
            current_group.append(tiles[i])
        else:
            if tiles[i].number == current_group[0].number:
                duplicate = False
                for tile in current_group:
                    if tile.color == tiles[i].color:
                        duplicate = True
                        break
                if not duplicate:
                    current_group.append(tiles[i])
            else:
                if len(current_group) >= 3:
                    return current_group

                # Moving on to a different number
                current_group.clear()
                current_group.append(tiles[i])

    if len(current_group) >= 3:
        return current_group

    return []


def is_run(tile_set):
    """Does this look like a run? No real error handling"""
    return tile_set[0].number != tile_set[1].number

def try_add_to_run_on_board(tile):
    for tile_set in board:
        if is_run(tile_set):
            if tile.color == tile_set[0].color:

                if tile.number == tile_set[0].number - 1:
                    tile_set.insert(0, tile)
                    return True
                if tile.number == tile_set[len(tile_set) - 1].number + 1:
                    tile_set.append(tile)
                    return True

                if len(tile_set) >= 5:
                    for i in range(len(tile_set)):
                        if tile_set[i] == tile:
                            if i >= 2 and i <= len(tile_set) - 3:
                                if print_verbosity > 5:
                                    print("Splitting tile set for tile: ", end="")
                                    tile.print()
                                    print("")
                                    print_tiles("  Original:", tile_set)
                                board.remove(tile_set)
                                tile_set.insert(i, tile)
                                board.append(tile_set[:i + 1])
                                board.append(tile_set[i + 1:])
                                if print_verbosity > 5:
                                    print_tiles("    left:", tile_set[:i + 1])
                                    print_tiles("    right :", tile_set[i + 1:])
                                return True

    return False


def try_add_to_group_on_board(tile):
    for tile_set in board:
        if not is_run(tile_set):
            if tile.number == tile_set[0].number:
                has_color = False
                for play_tile in tile_set:
                    if play_tile.color == tile.color:
                        has_color = True
                        break
                if not has_color:
                    tile_set.append(tile)
                    return True
    return False


def find_tile_sets(tiles):
    tile_sets = []
    while True:
        tile_set = find_run(tiles)
        if len(tile_set) > 0:
            remove_tiles(tiles, tile_set)
            tile_sets.append(tile_set)
        else:
            tile_set = find_group(tiles)
            if len(tile_set) > 0:
                remove_tiles(tiles, tile_set)
                tile_sets.append(tile_set)
            break
    return tile_sets


class Tile:
    number = 0
    color = 0

    def __lt__(self, other):
        """Default sort is by color, then by number."""
        if self.color == other.color:
            return self.number < other.number
        return self.color < other.color

    def __eq__(self, other):
        return self.number == other.number and self.color == other.color

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def print(self):
        print(f"{self.number}[{colors[self.color]}]", end=" ")


class Player:
    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.melded_turn = 0
        self.turns = 1

    def print(self):
        print_tiles(self.name + ":", self.tiles)

    def take_tiles(self, num_tiles):       
        try:
            for i in range(num_tiles):
                self.tiles.append(stacked_tiles.pop())
        except IndexError:
            pass

    def try_meld(self):
        total = 0
        tile_sets = find_tile_sets(self.tiles)
        for tile_set in tile_sets:
            for tile in tile_set:
                total = total + tile.number

        if total >= 30:
            print_tile_sets(f"{self.name} melded on turn {self.turns}:", tile_sets)
            board.extend(tile_sets)
            return True
        else:
            # Put the tiles back
            for tile_set in tile_sets:
                self.tiles.extend(tile_set)
        return False

    def try_play_tiles(self):
        played_tiles = []

        # First see if we have any standalone tile_sets
        tile_sets = find_tile_sets(self.tiles)
        if len(tile_sets) > 0:
            board.extend(tile_sets)
            for tile_set in tile_sets:
                for tile in tile_set:
                    played_tiles.append(tile)

        # Next, try to add onto other players' tiles
        i = 0
        while True:
            if i >= len(self.tiles):
                break
            
            if try_add_to_run_on_board(self.tiles[i]):
                played_tiles.append(self.tiles.pop(i))
                i = 0
            elif try_add_to_group_on_board(self.tiles[i]):
                played_tiles.append(self.tiles.pop(i))
                i = 0
            else:
                i = i + 1

        if len(played_tiles) > 0:
            print_tiles(f"{self.name} played tiles:", played_tiles)
            return True
        return False

    def play_turn(self):
        self.turns = self.turns + 1
        played_tile = False
        if self.melded_turn == 0:
            if self.try_meld():
                self.melded_turn = self.turns
                played_tile = True

        if self.melded_turn > 0:
            if self.try_play_tiles():
                played_tile = True

        if not played_tile:
            self.take_tiles(1)
            if print_verbosity > 5:
                print(f"{self.name} took a tile. {len(stacked_tiles)} remaining. tile = ", end="")
                self.tiles[len(self.tiles) - 1].print()
                print("")
        
        return played_tile


def create_initial_tiles(num_colors, duplicates_per_color, num_initial_tiles):
    tiles = []
    for c in range(num_colors):
        for i in range(1, max_tile_number + 1):
            for d in range(duplicates_per_color):
                tiles.append(Tile(i, c))
    random.shuffle(tiles)
    return tiles


def validate_board(num_colors, duplicates_per_color, num_initial_tiles):
    """Ensure that all tiles are accounted for"""
    all_tiles = create_initial_tiles(num_colors, duplicates_per_color, num_initial_tiles)
    for tile in stacked_tiles:
        all_tiles.remove(tile)

    for tile_set in board:
        assert(len(tile_set) >= 3)
        for tile in tile_set:
            all_tiles.remove(tile)

    for player in players:
        for tile in player.tiles:
            all_tiles.remove(tile)

    if len(all_tiles) > 0:
        print_tiles("Extra tiles:", all_tiles)
        assert(False)


def init_game(num_players, num_colors, duplicates_per_color, num_initial_tiles):
    board.clear()
    stacked_tiles.clear()
    players.clear()

    stacked_tiles.extend(create_initial_tiles(num_colors, duplicates_per_color, num_initial_tiles))
    if print_verbosity > 5:
        print(f"Total tiles: {len(stacked_tiles)}")

    for p in range(num_players):
        player = Player(f"Player{p}")
        player.take_tiles(num_initial_tiles)
        players.append(player)

    if print_verbosity > 5:
        print(f"Stacked tiles: {len(stacked_tiles)}")
    

def print_stats():
    print("")
    for player in players:
        if player.melded_turn > 0:
            print(f"{player.name}: melded on turn {player.melded_turn} and has {len(player.tiles)} tiles remaining")
            print_tiles("    Tiles:", player.tiles)
        else:
            print(f"{player.name}: NEVER MELDED and has {len(player.tiles)} tiles remaining")
            print_tiles("    Tiles: ", player.tiles)
            tile_sets = find_tile_sets(player.tiles)
            print_tile_sets("  Available tile_sets:", tile_sets)


def play_normal_game(num_players, num_colors, duplicates_per_color, num_initial_tiles):
    init_game(num_players, num_colors, duplicates_per_color, num_initial_tiles)

    final_draw = num_players

    for t in range(1000):
        player = players[t % len(players)]
        if player.play_turn():
            print_tile_sets(f"Board update for turn #{t}:", board)
            if len(player.tiles) == 0:
                print("*** RUMMIKUB!")
                break

        if len(stacked_tiles) == 0:
            if final_draw == 0:
                print("*** OUT OF TILES! NOBODY WON!")
                break
            final_draw = final_draw - 1

        validate_board(num_colors, duplicates_per_color, num_initial_tiles)

    print_stats()


if __name__ == '__main__':
    play_normal_game(num_players = 4, num_colors = 4, duplicates_per_color = 2, num_initial_tiles = 14)
