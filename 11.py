"""
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""

from dataclasses import dataclass


@dataclass
class Galaxy:
    row: int
    col: int

    def distance(self, other: "Galaxy") -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)


def expand_vertical(lines: list[str]) -> list[str]:
    """Expand the universe in the vertical direction"""
    expanded = []
    for line in lines:
        expanded.append(line)
        if "#" not in line:
            expanded.append(line)
    return expanded


def transpose(lines: list[str]) -> list[str]:
    """Transpose the universe"""
    return ["".join(line) for line in zip(*lines)]


def part_1(fp: str) -> int:
    with open(fp, "r") as f:
        lines = f.readlines()

    # expand empty rows
    lines = expand_vertical(lines)

    # transpose and expand rows again (no need to transpose back)
    lines = transpose(lines)
    lines = expand_vertical(lines)

    # find galaxies
    galaxies = []
    for row, line in enumerate(lines):
        for col, x in enumerate(line):
            if x == "#":
                galaxies.append(Galaxy(row, col))

    # sum the distances
    total = 0
    for idx, galaxy in enumerate(galaxies[:-1]):  # skip the last galaxy
        for other in galaxies[idx + 1 :]:
            total += galaxy.distance(other)

    return total


if __name__ == "__main__":
    # part 1
    print(part_1("11-01.txt"))
    print(part_1("11-02.txt"))
