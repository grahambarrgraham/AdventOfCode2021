from pathlib import Path
import sys

TEST_MODE = bool(len(sys.argv) > 1 and sys.argv[1] == "test")


def phase1(v):
    return search(v)


def phase2(v):
    return search(big_graph(v))


def search(v):
    target_node = (len(v[0]) - 1), len(v) - 1
    return a_star_algorithm(v, (0, 0), target_node)


def big_graph(v):

    new_v = [None] * len(v) * 5

    for y, line in enumerate(v):
        for i in range(1, 5):
            v[y] = v[y] + [inc_val(x, i) for x in line]

    for y, line in enumerate(v):
        for i in range(5):
            new_v[y + (i * len(v))] = [inc_val(x, i) for x in v[y]]

    return new_v


def inc_val(val, inc):
    ret = val
    for i in range(inc):
        ret = 1 if ret == 9 else ret + 1
    return ret


def all_nodes(v):
    ret = []
    for y in range(len(v)):
        for x in range(len(v[0])):
            ret.append((x, y))
    return ret


def find_neighbours(coord, v):
    x, y = coord
    return [(x + a, y + b) for a, b in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
            len(v[0]) > x + a >= 0 and len(v) > y + b >= 0]


def cost(coord, v):
    x, y = coord
    return v[y][x]


def distance(coord, target):
    return abs(target[0] - coord[0]) + abs(target[1] - coord[1])


def a_star_algorithm(graph, start, stop):
    open_lst = {start}
    closed_lst = set()
    poo = {start: 0}
    par = {start: start}

    while len(open_lst) > 0:
        n = None

        for v in open_lst:
            if n is None or poo[v] < poo[n]:
                n = v

        if n is None:
            print('Path does not exist!')
            return None

        if n == stop:
            return poo[n]

        for m in find_neighbours(n, graph):
            weight = cost(m, graph)
            if m not in open_lst and m not in closed_lst:
                open_lst.add(m)
                par[m] = n
                poo[m] = poo[n] + weight

            else:
                if poo[m] > poo[n] + weight:
                    poo[m] = poo[n] + weight
                    par[m] = n

                    if m in closed_lst:
                        closed_lst.remove(m)
                        open_lst.add(m)

        open_lst.remove(n)
        closed_lst.add(n)

    return None


if __name__ == "__main__":
    with Path(__file__).parent.joinpath("input/day15_sample" if TEST_MODE else "input/day15").open() as f:
        values = [[int(j) for j in list(i.strip())] for i in f]
        print(f'Phase 1: {phase1(values)}')
        print(f'Phase 2: {phase2(values)}')



