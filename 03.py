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

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
"""

from dataclasses import dataclass


@dataclass
class Symbol:
    what: str
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


def scan_schematic(fp: str) -> tuple[list[Number], list[Symbol]]:
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
                symbols.append(Symbol(what=c, x=x, y=y))

    return numbers, symbols


def part_1(fp: str) -> int:
    numbers, symbols = scan_schematic(fp)

    # check each number for adjacency to symbols
    total = 0
    for number in numbers:
        for symbol in symbols:
            if number.is_adjacent(symbol):
                total += number.value
                break

    return total


def part_2(fp: str) -> int:
    numbers, symbols = scan_schematic(fp)

    # check each * for adjacency to numbers
    stars = [s for s in symbols if s.what == "*"]
    total = 0
    for star in stars:
        ratio = 1
        num_adj = 0
        for number in numbers:
            if number.is_adjacent(star):
                ratio *= number.value
                num_adj += 1
        if num_adj == 2:
            total += ratio

    return total


if __name__ == "__main__":
    # part 1
    small_ans = part_1("03-01-small.txt")
    assert small_ans == 4361
    print(small_ans)
    print(part_1("03-01-large.txt"))

    # part 2
    small_ans = part_2("03-01-small.txt")
    assert small_ans == 467835
    print(small_ans)
    print(part_2("03-01-large.txt"))
