"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
"""

from dataclasses import dataclass

# From any of these tiles, you can add either tuple to traverse the path
valid_directions = {
    "|": ((-1, 0), (1, 0)),  # north and south
    "-": ((0, 1), (0, -1)),  # east and west
    "L": ((-1, 0), (0, 1)),  # north and east
    "J": ((-1, 0), (0, -1)),  # north and west
    "7": ((1, 0), (0, -1)),  # south and west
    "F": ((1, 0), (0, 1)),  # south and east
}


@dataclass
class Coord:
    row: int
    col: int

    def get_adjacent(self):
        """Return a list of 8 adjacent coordinates"""
        return [
            Coord(r, c)
            for r in range(self.row - 1, self.row + 2)
            for c in range(self.col - 1, self.col + 2)
            if (r, c) != (self.row, self.col)
        ]


@dataclass
class Node:
    coord: Coord  # row, col
    pipe: str  # |, -, L, J, 7, F, or S

    def get_connected_coords(self):
        """Return a list of 2 coordinates that are connected to this node"""
        return [
            Coord(self.coord.row + d[0], self.coord.col + d[1])
            for d in valid_directions.get(self.pipe, [])
        ]


def part_1(fp: str) -> int:
    with open(fp, "r") as f:
        lines = f.readlines()

    # pad with .
    lines = [f".{line.strip()}." for line in lines]
    lines = ["." * len(lines[0])] + lines + ["." * len(lines[0])]

    # find the start node
    start_1D = "".join(lines).index("S")
    start_coord = Coord(start_1D // len(lines[0]), start_1D % len(lines[0]))

    # search each node adjacent to S and pick the first one that connects to S
    for coord in start_coord.get_adjacent():
        node = Node(coord, lines[coord.row][coord.col])
        if start_coord in node.get_connected_coords():
            last_coord = start_coord
            break

    # traverse the nodes and track length until you reach S again
    distance = 1
    while node.pipe != "S":
        # find the next node
        for coord in node.get_connected_coords():
            if coord != last_coord:
                next_coord = coord
                break

        # update distance and move on
        distance += 1
        last_coord = node.coord
        node = Node(next_coord, lines[next_coord.row][next_coord.col])

    # take the total distance traveled, return half
    return distance // 2


if __name__ == "__main__":
    # part 1
    assert part_1("10-01.txt") == 4
    assert part_1("10-02.txt") == 4
    assert part_1("10-03.txt") == 8
    assert part_1("10-04.txt") == 8
    print(part_1("10-05.txt"))
