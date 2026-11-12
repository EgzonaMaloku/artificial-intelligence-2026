"""Sudoku Solver - Breadth First Search (BFS) me backtracking.

Gjendja eshte rrjeta 9x9 si 81 bajte (0 = qelize bosh). BFS i zgjeron gjendjet nivel pas niveli:
ne cdo nivel plotesohet edhe nje qelize. Backtracking-u eshte krasitja: nje femije krijohet vetem
nese vlera nuk perseritet ne rresht, kolone ose bllok, dhe nje gjendje me qelize pa asnje kandidat
eshte rruge pa dalje dhe hidhet, keshtu qe kerkimi nuk vazhdon kurre nga nje gjendje e pavlefshme.
"""

import argparse
import math
import time
from collections import deque

from puzzles import PUZZLES
from sudoku_validator import conflicts, validate

DIGITS = 0b1111111110
ROW = [i // 9 for i in range(81)]
COL = [i % 9 for i in range(81)]

BOX = [(i // 27) * 3 + (i % 9) // 3 for i in range(81)]


def parse(text):
    cells = [c for c in text if c in "0123456789."]
    if len(cells) != 81:
        raise ValueError(f"Sudoku duhet te kete 81 qeliza, jo {len(cells)}.")
    return bytes(0 if c == "." else int(c) for c in cells)


def masks(state):
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for i, v in enumerate(state):
        if v:
            bit = 1 << v
            rows[ROW[i]] |= bit
            cols[COL[i]] |= bit
            boxes[BOX[i]] |= bit
    return rows, cols, boxes


def candidates(i, rows, cols, boxes):
    return DIGITS & ~(rows[ROW[i]] | cols[COL[i]] | boxes[BOX[i]])


def count_bits(mask):
    return bin(mask).count("1")


def choose_cell(state, rows, cols, boxes, order):
    """fixed: qeliza e pare bosh (rresht pas rreshti). mrv: qeliza bosh me me pak kandidate."""
    if order == "fixed":
        i = state.index(0)
        return i, candidates(i, rows, cols, boxes)
    best, best_mask, best_count = -1, 0, 10
    for i, v in enumerate(state):
        if v == 0:
            mask = candidates(i, rows, cols, boxes)
            count = count_bits(mask)
            if count < best_count:
                best, best_mask, best_count = i, mask, count
                if count <= 1:
                    break
    return best, best_mask


def landscape(state):
    """Kthen (qeliza bosh, log10 e 9^k, log10 e prodhimit te kandidateve fillestare)."""
    empty = [i for i in range(81) if state[i] == 0]
    rows, cols, boxes = masks(state)
    counts = [count_bits(candidates(i, rows, cols, boxes)) for i in empty]
    log_cand = -math.inf if 0 in counts else sum(math.log10(c) for c in counts)
    return len(empty), len(empty) * math.log10(9), log_cand


def bfs(start, order="mrv", max_solutions=1, time_limit=60, max_frontier=3_000_000):
    """Kthen (zgjidhjet, statistikat, statusi). Statusi: solved, no_solution, timeout, memory."""
    stats = {"expanded": 0, "generated": 1, "dead_ends": 0, "max_frontier": 1, "depth": start.count(0)}
    if conflicts(start):
        return [], stats, "no_solution"
    if 0 not in start:
        return [start], stats, "solved"

    deadline = time.time() + time_limit
    frontier = deque([start])
    solutions = []
    while frontier:
        state = frontier.popleft()
        stats["expanded"] += 1
        if stats["expanded"] % 5000 == 0 and time.time() > deadline:
            return solutions, stats, "timeout"

        rows, cols, boxes = masks(state)
        i, mask = choose_cell(state, rows, cols, boxes, order)
        if mask == 0:
            stats["dead_ends"] += 1
            continue

        for v in range(1, 10):
            if mask >> v & 1:
                child = state[:i] + bytes((v,)) + state[i + 1:]
                stats["generated"] += 1
                if 0 in child:
                    frontier.append(child)
                else:
                    solutions.append(child)
                    if max_solutions and len(solutions) >= max_solutions:
                        return solutions, stats, "solved"

        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
        if len(frontier) > max_frontier:
            return solutions, stats, "memory"

    return solutions, stats, ("solved" if solutions else "no_solution")


def format_grid(state):
    lines = []
    for r in range(9):
        if r and r % 3 == 0:
            lines.append("------+-------+------")
        row = [str(state[r * 9 + c] or ".") for c in range(9)]
        lines.append(" ".join(row[0:3]) + " | " + " ".join(row[3:6]) + " | " + " ".join(row[6:9]))
    return "\n".join(lines)


def solve_and_report(name, puzzle, args):
    empty, log_raw, log_cand = landscape(puzzle)
    print(f"=== {name}: {81 - empty} numra te dhene, {empty} qeliza bosh")
    print(f"Landscape: 9^{empty} = 10^{log_raw:.1f}, me kandidatet fillestare = 10^{log_cand:.1f}")
    print(format_grid(puzzle))

    start = time.time()
    max_solutions = 0 if args.all else 1
    solutions, stats, status = bfs(puzzle, args.order, max_solutions, args.time, args.max_frontier)
    elapsed = time.time() - start

    print(
        f"\nBFS ({args.order}): {status}, {elapsed:.2f}s, "
        f"{stats['expanded']} nyje te zgjeruara, {stats['generated']} te gjeneruara, "
        f"{stats['dead_ends']} rruge pa dalje, frontier maksimal {stats['max_frontier']}, "
        f"thellesia {stats['depth']}"
    )
    if args.all and status in ("solved", "no_solution"):
        print(f"Numri i zgjidhjeve: {len(solutions)}")
    if solutions:
        errors = validate(solutions[0], puzzle)
        print(f"Validimi: f = {conflicts(solutions[0])}, {'e vlefshme' if not errors else errors}")
        print(format_grid(solutions[0]))
    print()


def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver me BFS dhe backtracking")
    parser.add_argument("-l", "--level", choices=["easy", "medium", "hard", "all"], default="all")
    parser.add_argument("--puzzle", help="sudoku si 81 karaktere (0 ose . per qelize bosh)")
    parser.add_argument("--order", choices=["mrv", "fixed"], default="mrv",
                        help="mrv: qeliza me me pak kandidate; fixed: rresht pas rreshti")
    parser.add_argument("--all", action="store_true", help="gjej te gjitha zgjidhjet (kontrollon unicitetin)")
    parser.add_argument("-t", "--time", type=float, default=60, help="limiti i kohes per sudoku (sekonda)")
    parser.add_argument("--max-frontier", type=int, default=3_000_000)
    args = parser.parse_args()

    if args.puzzle:
        solve_and_report("Custom", parse(args.puzzle), args)
        return
    levels = ["easy", "medium", "hard"] if args.level == "all" else [args.level]
    for level in levels:
        text, source = PUZZLES[level]
        solve_and_report(f"{level.capitalize()} ({source})", parse(text), args)


if __name__ == "__main__":
    main()
