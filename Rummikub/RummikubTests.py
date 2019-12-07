import re
import unittest
import RummikubSimulator as rs

def parse_tile(tile_string):
    match = re.match(r"([)0-9]+)\[([a-z]+)\]", tile_string)
    return rs.Tile(int(match.group(1)), rs.colors.index(match.group(2)))


def parse_tiles(tiles_string):
    tiles = []
    tile_string_list = tiles_string.split(' ')
    for tile_string in tile_string_list:
        tiles.append(parse_tile(tile_string))
    return tiles


class TestFindingRuns(unittest.TestCase):

    def test_find_minimal_run(self):
        tiles = parse_tiles("1[blue] 2[blue] 3[blue]")
        found_run = rs.find_run(tiles)
        self.assertEquals(len(tiles), len(found_run))

    def test_find_expanded_run(self):
        tiles = parse_tiles("1[blue] 2[blue] 3[blue] 4[blue] 5[blue]")
        found_run = rs.find_run(tiles)
        self.assertEquals(len(tiles), len(found_run))

    def test_no_run_too_few(self):
        tiles = parse_tiles("1[blue] 2[blue]")
        found_run = rs.find_run(tiles)
        self.assertEquals(len(found_run), 0)

    def test_no_run_present(self):
        tiles = parse_tiles("1[blue] 2[blue] 4[blue]")
        found_run = rs.find_run(tiles)
        self.assertEquals(len(found_run), 0)


class TestFindingGroups(unittest.TestCase):

    def test_find_minimal_group(self):
        tiles = parse_tiles("1[blue] 1[red] 1[green]")
        found_group = rs.find_group(tiles)
        self.assertEqual(len(tiles), len(found_group))


class TestSplits(unittest.TestCase):

    def test_split_at_end(self):
        rs.board.clear()
        rs.board.append(parse_tiles("8[orange] 9[orange] 10[orange] 11[orange] 12[orange] 13[orange]"))
        rs.try_add_to_run_on_board(parse_tile("11[orange]"))


class TestPlayerMelds(unittest.TestCase):

    def test_minimal_run_meld(self):
        # TODO: Refactor so board isn't global
        rs.board.clear()
        player = rs.Player("TestPlayer")
        player.tiles = parse_tiles("9[blue] 10[blue] 11[blue]")
        self.assertTrue(player.try_meld())

    def test_close_but_insufficient_run_meld(self):
        # TODO: Refactor so board isn't global
        rs.board.clear()
        player = rs.Player("TestPlayer")
        player.tiles = parse_tiles("8[blue] 9[blue] 10[blue]")
        self.assertFalse(player.try_meld())


if __name__ == '__main__':
    unittest.main()
