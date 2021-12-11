from pathlib import Path
import sys
import copy

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return sum([len(generation_step(v, gen + 1)) for gen in range(100)])


def phase2(v):
    gen = 1
    all_octopuses = len(all_coords(v))
    while True:
        flashed = generation_step(v, gen)
        if len(flashed) == all_octopuses:
            break
        gen = gen + 1

    return gen


def generation_step(v, gen):
    candidates = all_coords(v)
    flashed = set()
    while True:
        generate(candidates, v)
        flashes = {(x, y) for (x, y) in candidates if v[y][x] > 9 and (x, y) not in flashed}
        reset_flashed(flashes, v)
        # print_grid(v, candidates, flashes, flashed, gen)
        if len(flashes) > 0:
            flashed = flashed.union(flashes)
            candidates = [(x, y) for (x, y) in flatten([neighbours(flash, v) for flash in flashes]) if
                          (x, y) not in flashed]
        else:
            break
    return flashed


def print_grid(v, neighbours, flashes, flashed, gen):

    print()
    print("Generation", gen)

    def format(coord, val):
        if coord in flashes:
            return red(val)
        elif coord in neighbours:
            return green(val)
        elif coord in flashed:
            return yellow(val)
        else:
            return val

    def red(val):
        return '\033[91m' + val + '\033[0m'

    def green(val):
        return '\033[92m' + val + '\033[0m'

    def yellow(val):
        return '\033[93m' + val + '\033[0m'

    for y, line in enumerate(v):
        zz = enumerate(v[y])
        y_ = [format((x, y), str(val)) for x, val in zz]
        print(''.join(y_))


def flatten(t):
    return [item for sublist in t for item in sublist]


def all_coords(v):
    return [(x, y) for y in range(len(v)) for x in range(len(v[0]))]


def neighbours(coord, v):
    (x, y) = coord
    return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)] if
            len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]


def reset_flashed(coords, v):
    for (x, y) in coords:
        if v[y][x] > 9:
            v[y][x] = 0


def generate(coords, v):
    for (x, y) in coords:
        v[y][x] = v[y][x] + 1


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day11_sample" if TEST_MODE else "input/day11").open() as f:
        values = [[int(j) for j in i.strip()] for i in f]
        print(f'Phase 1: {phase1(copy.deepcopy(values))}')
        print(f'Phase 2: {phase2(copy.deepcopy(values))}')
