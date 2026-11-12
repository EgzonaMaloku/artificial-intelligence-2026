"""Validimi i nje zgjidhjeje Sudoku dhe funksioni objektiv f."""

ROWS = [[r * 9 + c for c in range(9)] for r in range(9)]
COLS = [[r * 9 + c for r in range(9)] for c in range(9)]
BOXES = [
    [(br * 3 + r) * 9 + bc * 3 + c for r in range(3) for c in range(3)]
    for br in range(3)
    for bc in range(3)
]
UNITS = ROWS + COLS + BOXES


def conflicts(grid):
    """Funksioni objektiv: f = sum mbi 27 njesite e sum max(0, count(v) - 1). Qelizat bosh (0) injorohen."""
    f = 0
    for unit in UNITS:
        counts = [0] * 10
        for i in unit:
            counts[grid[i]] += 1
        f += sum(max(0, c - 1) for c in counts[1:])
    return f


def validate(solution, puzzle):
    """Kthen listen e gabimeve; lista bosh do te thote qe zgjidhja eshte e vlefshme."""
    errors = []
    if len(solution) != 81:
        return [f"Rrjeta ka {len(solution)} qeliza, jo 81."]
    if 0 in solution:
        errors.append(f"Ka {list(solution).count(0)} qeliza bosh.")
    changed = [i for i in range(81) if puzzle[i] and puzzle[i] != solution[i]]
    if changed:
        errors.append(f"Jane ndryshuar {len(changed)} numra te dhene.")
    f = conflicts(solution)
    if f:
        errors.append(f"Ka {f} perseritje ne rreshta, kolona ose blloqe (f = {f}).")
    return errors


if __name__ == "__main__":
    solved = bytes(int(c) for c in "534678912672195348198342567859761423426853791713924856961537284287419635345286179")
    broken = bytearray(solved)
    broken[0], broken[1] = broken[1], broken[0]
    print("E sakta:", validate(solved, bytes(81)) or "e vlefshme")
    print("E prishura:", validate(bytes(broken), bytes(81)) or "e vlefshme")
