"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

from dataclasses import dataclass


@dataclass
class Symbol:
    x: int
    y: int


@dataclass
class Number:
    value: int
    x_start: int
    x_end: int
    y: int

    def is_adjacent(self, s: Symbol) -> bool:
        return (
            self.x_start - 1 <= s.x <= self.x_end + 1
            and self.y - 1 <= s.y <= self.y + 1
        )


def part_1(fp: str) -> int:
    with open(fp, "r") as f:
        lines = f.readlines()

    # To simplify the algorithm, pad the schematic with periods
    lines = [f".{line.strip()}." for line in lines]
    lines = ["." * len(lines[0])] + lines + ["." * len(lines[0])]

    # scan for numbers and symbols
    numbers = []
    symbols = []
    for y, line in enumerate(lines):
        # skip first and last lines
        if y == 0 or y == len(lines) - 1:
            continue
        digit_start = None
        for x, c in enumerate(line):
            if not digit_start and c.isdigit():
                digit_start = x
            elif digit_start and not c.isdigit():
                numbers.append(
                    Number(
                        value=int(line[digit_start:x]),
                        x_start=digit_start,
                        x_end=x - 1,
                        y=y,
                    )
                )
                digit_start = None
            if not digit_start and not c.isdigit() and c != ".":
                symbols.append(Symbol(x=x, y=y))

    # check each number for adjacency to symbols
    total = 0
    for number in numbers:
        for symbol in symbols:
            if number.is_adjacent(symbol):
                total += number.value
                break

    return total


if __name__ == "__main__":
    # part 1
    small_ans = part_1("03-01-small.txt")
    assert small_ans == 4361
    print(small_ans)
    print(part_1("03-01-large.txt"))
