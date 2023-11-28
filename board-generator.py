import argparse
from itertools import product
import math
import random
import re

VALID_PIECES = {"Q"}
CELL_PATTERN = re.compile(r"^([a-zA-Z]+)(\d+):(Q)$")


def alphabetic_to_index(string):
    index = 0
    for char in string:
        index = index * 26 + ord(char.lower()) - ord("a") + 1
    return index - 1


def index_to_alphabetic(index):
    result = ""
    while index >= 0:
        remainder = index % 26
        result = chr(ord("A") + remainder) + result
        index = index // 26 - 1
    return result


def parse_chess_cell(cell_str):
    try:
        column, row, piece = CELL_PATTERN.match(cell_str).groups()
    except AttributeError:  # when the match is None
        raise argparse.ArgumentError(f"Invalid format {cell_str} for a cell")

    if piece not in VALID_PIECES:
        raise argparse.ArgumentError(f"Piece {piece} not supported")

    cell = (int(row), alphabetic_to_index(column))

    return (cell, piece)


def int_larger_than_0(str_value):
    value = int(str_value)
    if value <= 0:
        raise ValueError("Expected a value larger than 0")
    return value


def main():
    parser = argparse.ArgumentParser(description="Board generator")
    parser.add_argument(
        "N", type=int_larger_than_0, help="Positive integer N (size of the board)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--piece_cells",
        type=parse_chess_cell,
        nargs="*",
        help="List of cells with chess pieces" ' (e.g., "A1:Q, B2:R, C3:B")',
    )
    group.add_argument(
        "--random-queens",
        type=int,
        metavar="X",
        help="Add X queens randomly in the board."
    )
    args = parser.parse_args()


    if args.piece_cells:
        for (row, column), piece in args.piece_cells:
            if row >= args.N or column >= args.N:
                cell_str = f"{index_to_alphabetic(column)}{row}"
                parser.error(f"Cell {cell_str} outside the {args.N}x{args.N} board")

        pieces = dict(args.piece_cells)
    else:
        all_cells = [cell for cell in product(range(args.N), range(args.N))]
        queens = random.choices(
            all_cells,
            k=args.random_queens
        )
        pieces = {cell: "Q" for cell in queens}

    print(f"n {args.N}")
    for row in range(args.N):
        for col in range(args.N):
            print(pieces.get((row, col), "-"), end=" ")
        print("")


if __name__ == "__main__":
    main()
