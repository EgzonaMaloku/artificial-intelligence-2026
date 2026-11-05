"""Social Golfers Problem - DFS me backtracking.

n = g * p lojtare, g grupe me nga p lojtare, w jave.
Dy lojtare nuk duhet te jene ne te njejtin grup me shume se nje here.

Dy menyra:
  - DFS sistematik: provon kandidatet me radhe; nese e shteron pemen, w eshte e pamundur.
  - DFS me rinisje te rastesishme (--random): renditje e rastesishme e kandidateve dhe
    rinisje sa here kalohet nje numer nyjesh. Gjen me shpejt orare me shume jave,
    por nuk mund te provoje qe nje w eshte e pamundur.
"""

import argparse
import random
import time

from solution_validator import conflicts, validate


class SearchLimit(Exception):
    pass


def dfs_schedule(g, p, w, deadline, node_limit=None, rng=None):
    """Kthen (orari ose None, numri i nyjeve). Hedh SearchLimit kur kalohet koha ose nyjet."""
    n = g * p
    met = [0] * n
    used = [0] * w
    sched = [[[] for _ in range(g)] for _ in range(w)]
    nodes = 0

    def candidates(week, grp):
        if not grp or week == 0:
            # simetria: lojtari i pare = me i vogli i pavendosur; java 1 fiksohet
            return [next(i for i in range(n) if not used[week] >> i & 1)]
        cand = [x for x in range(grp[-1] + 1, n) if not used[week] >> x & 1]
        if rng:
            rng.shuffle(cand)
        return cand

    def dfs(week, group):
        nonlocal nodes
        nodes += 1
        if node_limit and nodes > node_limit:
            raise SearchLimit
        if nodes % 2000 == 0 and time.time() > deadline:
            raise SearchLimit
        if week == w:
            return True
        if group == g:
            return dfs(week + 1, 0)
        grp = sched[week][group]
        if len(grp) == p:
            return dfs(week, group + 1)

        mask = 0
        for y in grp:
            mask |= 1 << y

        for x in candidates(week, grp):
            if met[x] & mask:
                continue
            met[x] |= mask
            for y in grp:
                met[y] |= 1 << x
            used[week] |= 1 << x
            grp.append(x)

            if dfs(week, group):
                return True

            grp.pop()
            used[week] &= ~(1 << x)
            met[x] &= ~mask
            for y in grp:
                met[y] &= ~(1 << x)
        return False

    found = dfs(0, 0)
    return (sched if found else None), nodes


def solve(g, p, w, time_limit, randomized=False, restart_nodes=50_000, seed=None):
    """Kthen (orari, statusi, nyjet gjithsej, rinisjet). Statusi: found, impossible, timeout."""
    deadline = time.time() + time_limit
    if not randomized:
        try:
            sched, nodes = dfs_schedule(g, p, w, deadline)
        except SearchLimit:
            return None, "timeout", None, 0
        return sched, ("found" if sched else "impossible"), nodes, 0

    rng = random.Random(seed)
    total, restarts = 0, 0
    while time.time() < deadline:
        try:
            sched, nodes = dfs_schedule(g, p, w, deadline, restart_nodes, rng)
            total += nodes
            if sched:
                return sched, "found", total, restarts
            return None, "impossible", total, restarts
        except SearchLimit:
            total += restart_nodes
        restarts += 1
    return None, "timeout", total, restarts


def print_schedule(schedule):
    for i, week in enumerate(schedule, 1):
        groups = " | ".join(",".join(map(str, grp)) for grp in week)
        print(f"  Java {i:2}: {groups}")


def main():
    parser = argparse.ArgumentParser(description="Social Golfers Problem me DFS dhe backtracking")
    parser.add_argument("-g", "--groups", type=int, default=8)
    parser.add_argument("-p", "--size", type=int, default=4)
    parser.add_argument("-t", "--time", type=float, default=60, help="limiti i kohes per cdo w (sekonda)")
    parser.add_argument("--random", action="store_true", help="renditje e rastesishme me rinisje")
    parser.add_argument("--restart-nodes", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--from", dest="start", type=int, default=1, help="w e pare qe provohet")
    args = parser.parse_args()

    g, p = args.groups, args.size
    n = g * p
    upper_bound = (n - 1) // (p - 1)
    mode = "DFS me rinisje te rastesishme" if args.random else "DFS sistematik"

    print(f"Social Golfers: {n} lojtare, {g} grupe x {p}, kufiri teorik = {upper_bound} jave")
    print(f"Menyra: {mode}, limiti i kohes per cdo w: {args.time}s\n")

    best = None
    for w in range(args.start, upper_bound + 1):
        start = time.time()
        sched, status, nodes, restarts = solve(
            g, p, w, args.time, args.random, args.restart_nodes, args.seed
        )
        elapsed = time.time() - start
        info = f"{elapsed:.2f}s"
        if nodes is not None:
            info += f", {nodes} nyje"
        if args.random:
            info += f", {restarts} rinisje"

        if status != "found":
            reason = "pema u shterua, e pamundur" if status == "impossible" else "kaloi limiti i kohes"
            print(f"w = {w:2}: nuk u gjet zgjidhje - {reason} ({info})")
            break
        errors = validate(sched, g, p)
        print(f"w = {w:2}: OK, f = {conflicts(sched)}, {'valid' if not errors else errors} ({info})")
        best = sched

    if best:
        print(f"\nOrari me i mire i gjetur: {len(best)} jave")
        print_schedule(best)


if __name__ == "__main__":
    main()
