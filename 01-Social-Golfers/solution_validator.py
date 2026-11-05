"""Validimi i nje orari per Social Golfers Problem dhe funksioni objektiv f."""

from itertools import combinations


def conflicts(schedule):
    """Funksioni objektiv: f = sum max(0, takime(i,j) - 1). Orari eshte zgjidhje kur f = 0."""
    counts = {}
    for week in schedule:
        for grp in week:
            for pair in combinations(sorted(grp), 2):
                counts[pair] = counts.get(pair, 0) + 1
    return sum(max(0, c - 1) for c in counts.values())


def validate(schedule, g, p):
    """Kthen listen e gabimeve; lista bosh do te thote qe orari eshte i vlefshem."""
    n = g * p
    errors = []
    for w, week in enumerate(schedule, 1):
        if len(week) != g:
            errors.append(f"Java {w} ka {len(week)} grupe, jo {g}.")
        players = [x for grp in week for x in grp]
        if sorted(players) != list(range(n)):
            errors.append(f"Java {w} nuk i permban te gjithe lojtaret saktesisht nje here.")
        for i, grp in enumerate(week, 1):
            if len(grp) != p:
                errors.append(f"Grupi {i} ne javen {w} ka {len(grp)} lojtare, jo {p}.")
    f = conflicts(schedule)
    if f:
        errors.append(f"Ka {f} takime te perseritura (f = {f}).")
    return errors


if __name__ == "__main__":
    example = [
        [[0, 1], [2, 3]],
        [[0, 2], [1, 3]],
        [[0, 3], [1, 2]],
    ]
    errors = validate(example, g=2, p=2)
    print("Orari eshte i vlefshem." if not errors else "\n".join(errors))
